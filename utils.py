def trim(x):
    y = ""
    for c in x:
        if c <= "\u0020":
            if len(y) and y[-1] != " ":
                y += " "
            continue
        y += c
    if len(y) and y[-1] == " ":
        y = y[:-1]
    return y

def isnumeric(x):
    if not x:
        return False
    for c in x:
        if "0" <= c <= "9":
            continue
        return False
    return True

def isalpha_latin(x):
    if not x:
        return False
    for c in x:
        if "A" <= c <= "Z":
            continue
        if "a" <= c <= "z":
            continue
        return False
    return True

def isalpha_cjk(x):
    if not x:
        return False
    for c in x:
        if "ㄱ" <= c <= "ㅎ":
            continue
        if "가" <= c <= "힣":
            continue
        return False
    return True

def ngram_iter(x, sizes):
    for j in sizes:
        for i in range(len(x) - j):
            yield x[i:i + j]

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
