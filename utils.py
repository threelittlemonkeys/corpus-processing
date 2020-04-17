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

def ngram_iter(x, maxlen):
    for j in range(maxlen):
        for i in range(len(x) - j):
            yield x[i:i + j]

class tree():
    def __init__():
        self.children = list()
    
