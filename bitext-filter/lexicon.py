import os
import sys
import re

class lexicon(): # bilingual lexicon
    def __init__(self, src_lang, tgt_lang):
        self.path = (os.path.dirname(__file__) or ".") + "/"
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.data = dict()
        self.load_data("lexicon.%s%s" % (src_lang, tgt_lang))
        self.maxlen = max(map(len, self.data))

    def load_data(self, filename):
        fo = open(self.path + filename + ".tsv")
        for line in fo:
            src, *tgt = line.strip().split("\t")
            src = src.lower()
            tgt = [w.lower().replace(" ", "") for w in tgt]
            self.data[src] = tgt
        fo.close()

    def search(self, src, tgt):
        m = dict()
        i = 0
        while i < len(src):
            for j in range(self.maxlen, 0, -1):
                w = " ".join(src[i:i + j])
                if w in self.data:
                    m[w] = None
                    i += j
                    break
            else:
                i += 1
        if not m:
            return m
        for a in m:
            for b in self.data[a]:
                if b in tgt:
                    m[a] = b
                    break
        return m
