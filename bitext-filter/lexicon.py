import os
import sys
import re

class lexicon(): # bilingual lexicon
    def __init__(self, src_lang, tgt_lang):
        self.path = (os.path.dirname(__file__) or ".") + "/"
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.data = dict()
        self.maxlen = 0
        self.load_data("lexicon.%s%s" % (src_lang, tgt_lang))

    def load_data(self, filename):
        filename = self.path + filename + ".tsv"
        if not os.path.isfile(filename):
            return
        fo = open(filename)
        for i, line in enumerate(fo):
            if not re.match("^[^\t]+(\t[^\t]+)*\n", line):
                sys.exit("Error: invalid format in %s" % filename)
            a0, *b0 = line.strip().split("\t")
            a1 = a0.lower()
            b1 = [w.lower().replace(" ", "") for w in b0]
            if not b1:
                b0.append(a0)
                b1.append(a1)
            self.data[a1] = [a0, b0, b1]
        fo.close()
        self.maxlen = max(map(len, self.data))

    def search(self, src, tgt):
        m0 = dict()
        m1 = dict()
        i = 0
        while i < len(src):
            for j in range(self.maxlen, 0, -1):
                a1 = " ".join(src[i:i + j])
                if a1 in self.data:
                    a0, b0, b1 = self.data[a1]
                    m0[a0] = b0
                    for b1 in b1:
                        if b1 in tgt:
                            m1[a0] = b1
                            break
                    i += j
                    break
            else:
                i += 1
        return m0, m1
