import os
import sys
import re
from utils import *

class bilingual_lexicon(): # bilingual lexicon
    def __init__(self, src_lang, tgt_lang):
        self.path = os.path.dirname(__file__) + "/"
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

            if self.tgt_lang in CJK_LANGS:
                b1 = [w.lower().replace(" ", "") for w in b0]
            else:
                b1 = [w.lower() for w in b0]

            if not b1:
                b0.append(a0)
                b1.append(a1)

            if self.tgt_lang == "ru":
                b0 += [stem(w, self.tgt_lang) for w in b0]
                b1 += [stem(w, self.tgt_lang) for w in b1]

            self.data[a1] = [a0, set(b0), set(b1)]

        fo.close()

        self.maxlen = max(map(lambda x: x.count(" "), self.data)) + 1

    def search(self, src, tgt):
        m0 = dict()
        m1 = dict()

        sep = " "
        if self.tgt_lang in CJK_LANGS:
            sep = ""
        if self.tgt_lang == "ru":
            tgt = [stem(w, self.tgt_lang) for w in tgt]
        tgt = sep.join(tgt)

        i = 0
        while i < len(src):
            for j in range(min(len(src), i + self.maxlen), i, -1):
                a1 = " ".join(src[i:j])
                if a1 in self.data:
                    a0, b0, b1 = self.data[a1]
                    m0[a0] = b0
                    for w in b1:
                        if w in tgt:
                            m1[a0] = w
                            break
                    i += j
                    break
            else:
                i += 1

        return m0, m1
