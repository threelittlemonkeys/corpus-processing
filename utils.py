import sys

def sizeof(x, xids = set()):
    z = sys.getsizeof(x)
    xid = id(x)
    if xid in xids:
        return 0
    xids.add(xid)
    if isinstance(x, dict):
        z += sum([sizeof(k, xids) for k in x.keys()])
        z += sum([sizeof(v, xids) for v in x.values()])
    elif hasattr(x, '__dict__'):
        z += sizeof(x.__dict__, xids)
    elif hasattr(x, '__iter__') and not isinstance(x, (str, bytes, bytearray)):
        z += sum([sizeof(i, xids) for i in x])
    return z

def trim(s):
    y = ""
    for c in s:
        if c <= "\u0020":
            if len(y) and y[-1] != " ":
                y += " "
            continue
        y += c
    if len(y) and y[-1] == " ":
        y = y[:-1]
    return y

def isnumeric(s):
    if not s:
        return False
    for c in s:
        if "0" <= c <= "9":
            continue
        return False
    return True

def isalpha_latin(s):
    if not s:
        return False
    for c in s:
        if "A" <= c <= "Z":
            continue
        if "a" <= c <= "z":
            continue
        return False
    return True

def isalpha_cjk(s):
    if not s:
        return False
    for c in s:
        if "ㄱ" <= c <= "ㅎ":
            continue
        if "가" <= c <= "힣":
            continue
        return False
    return True

def ngram_iter(s, sizes):
    for j in sizes:
        for i in range(len(s) - j):
            yield s[i:i + j]

class lexicon_node():
    def __init__(self):
        self.children = dict()
        self.features = list()

class lexicon():
    def __init__(self):
        self.node = lexicon_node()
        self.size = 0

    def add(self, entry, feature):
        node = self.node
        for word in entry:
            if word not in node.children:
                node.children[word] = lexicon_node()
            node = node.children[word]
        if not node.features:
            self.size += 1
        node.features.append(feature)
        return node

    def find(self, entry):
        node = self.node
        for word in entry:
            if word not in node.children:
                return None
            node = node.children[word]
        return node
