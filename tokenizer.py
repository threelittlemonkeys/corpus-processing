import os
import sys
from collections import defaultdict

debug = True

lxc = dict()
lxc_fn = sys.path[0] + "/lexicon.tsv"
lxc_maxlen = 0

def init():
    load_dict(lxc_fn)

def load_dict(fn):
    global lxc_maxlen
    fo = open(fn)
    for x in fo:
        x = x.strip()
        lxc[x] = True
        if len(x) > lxc_maxlen:
            lxc_maxlen = len(x)
    fo.close()

def tokenize(txt):
    idx = [i for i, c in enumerate(txt) if c != " "]
    txt = txt.replace(" ", "")
    tbl = [[] for _ in txt]
    for i in range(len(txt)):
        k = min(len(txt), i + lxc_maxlen)
        for j in range(i + 1, k):
            w = txt[i:j]
            if w in lxc:
                tbl[i].append(w)
    return txt, idx, tbl

def analyze(raw):
    txt, idx, tbl = tokenize(raw)
    print("sent =", raw)
    print("norm =", txt)
    for i, x in enumerate(tbl):
        print("table[%d] =" % i, x)
    input()

if __name__ == "__main__":
    init()
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        analyze(line)
    fo.close()
