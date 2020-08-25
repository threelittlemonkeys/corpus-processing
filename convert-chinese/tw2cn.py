import sys
import re

class convert_chinese():
    def __init__(self, char_dict, word_dict, ignore_space = False):
        self.dict = dict()
        self.load_dict(char_dict)
        self.load_dict(word_dict)
        self.ignore_space = ignore_space
        self.re_bpmf = re.compile("[\u3105-\u312F]")

    def load_dict(self, filename):
        fo = open(filename)
        for line in fo:
            line = line.strip()
            a, b = line.split("\t")
            self.dict[a] = b
        fo.close()

    def bpmf_exists(self, line):
        return self.re_bpmf.search(line)

    def convert(self, line):
        sp = " " * self.ignore_space
        idx = [i for i, c in enumerate(line) if c != sp]
        norm = line.replace(sp, "")
        maxlen = max(map(len, self.dict))
    
        i = 0
        while i < len(norm):
            matched = list()
            for j in range(min((len(norm) - i), maxlen)):
                w = norm[i:i + j + 1]
                if w in self.dict:
                    matched.append(w)
            if not matched:
                i += 1
                continue
            src = max(matched, key = len)
            tgt = self.dict[src]
            k = idx[i] + len(tgt) - idx[i + len(src) - 1] - 1
            idx_l = idx[:i]
            idx_m = [idx[i] + j for j, c in enumerate(tgt) if c != " "]
            idx_r = [j + k for j in idx[i + len(src):]]
            norm_l = norm[:i]
            norm_m = tgt.replace(" ", "")
            norm_r = norm[i + len(src):]
            idx = idx_l + idx_m + idx_r
            norm = norm_l + norm_m + norm_r
            i += len(norm_m)
    
        out = ""
        for i, c in zip(idx, norm):
            out += " " * (i - len(out)) + c
    
        return out

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s text" % sys.argv[0])
    tw2cn = convert_chinese(
        char_dict = "fan2jian.tsv",
        word_dict = "tw2cn.tsv",
    )
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        if tw2cn.bpmf_exists(line):
            pass
        converted = tw2cn.convert(line)
        print(converted)
    fo.close()
