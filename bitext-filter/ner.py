import os
import sys
import re

class bilingual_ner():
    def __init__(self, src_lang, tgt_lang):
        self.path = (os.path.dirname(__file__) or ".") + "/"
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.dict = dict()
        self.load_dict("ner.%s%s" % (src_lang, tgt_lang))
        self.maxlen = max(map(len, self.dict))

    def load_dict(self, filename):
        fo = open(self.path + filename + ".tsv")
        for line in fo:
            src, *tgt = line.strip().split("\t")
            src = src.lower()
            tgt = [w.lower().replace(" ", "") for w in tgt]
            self.dict[src] = tgt
        fo.close()

    def search(self, src, tgt):
        ne = dict()
        i = 0
        while i < len(src):
            for j in range(self.maxlen, 0, -1):
                w = " ".join(src[i:i + j])
                if w in self.dict:
                    ne[w] = None
                    i += j
                    break
            else:
                i += 1
        if not ne:
            return ne
        for a in ne:
            for b in self.dict[a]:
                if b in tgt:
                    ne[a] = b
                    break
        return ne
