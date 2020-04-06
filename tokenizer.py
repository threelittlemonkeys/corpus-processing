import os
import sys
from collections import defaultdict

class tokenizer():

    def __init__(self, lexicon):
        self.lexicon = dict()
        self.lexicon_maxlen = 0
        self.debug = True
        self.load_lexicon(lexicon)

    def load_lexicon(self, filename):
        fo = open(filename)
        for x in fo:
            x = x.strip().split("\t")[0]
            self.lexicon[x] = True
            if len(x) > self.lexicon_maxlen:
                self.lexicon_maxlen = len(x)
        fo.close()

    def index(self, sent):
        idx = [x for x in enumerate(sent) if x[1] != " "]
        return idx
    
    def lexicalize(self, idx):
        table = [[] for _ in idx]
        for i in range(len(idx)):
            k = min(len(idx), i + self.lexicon_maxlen)
            for j in range(i + 1, k):
                w = "".join(c for _, c in idx[i:j])
                if w in self.lexicon:
                    table[i].append(w)
        return table
    
    def analyze(self, sent):
        idx = self.index(sent)
        table = self.lexicalize(idx)
        print("sent =", sent)
        print("norm =", "".join(c for _, c in idx))
        for i, x in enumerate(table):
            print("table[%d] =" % i, x)
        input()

if __name__ == "__main__":
    tokenizer = tokenizer(
        lexicon = sys.path[0] + "/lexicon.tsv"
    )
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        tokenizer.analyze(line)
    fo.close()
