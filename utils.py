import sys

def sizeof(x, xs = set()):
    z = sys.getsizeof(x)
    xid = id(x)
    if xid in xs:
        return 0
    xs.add(xid)
    if isinstance(x, dict):
        z += sum(sizeof(k, xs) for k in x.keys())
        z += sum(sizeof(v, xs) for v in x.values())
    elif hasattr(x, '__dict__'):
        z += sizeof(x.__dict__, xs)
    elif hasattr(x, '__iter__') and not isinstance(x, (str, bytes, bytearray)):
        z += sum(sizeof(i, xs) for i in x)
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

class lexicon():
    def __init__(self):
        self.node = [None, None]
        self.size = 0

    def add(self, entry, feature):
        node = self.node
        for word in entry:
            if not node[0]:
                node[0] = dict()
            if word not in node[0]:
                node[0][word] = [None, None]
            node = node[0][word]
        if not node[1]:
            node[1] = list()
            self.size += 1
        node[1].append(feature)
        return node

    def find(self, entry):
        node = self.node
        for word in entry:
            if not (node[0] and word in node[0]):
                return None
            node = node[0][word]
        return node[1]
