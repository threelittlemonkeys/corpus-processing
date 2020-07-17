import sys
import re

def load_dict(do, filename):
    fo = open(filename)
    for line in fo:
        line = line.strip()
        a, b = line.split("\t")
        do[a] = b
    fo.close()

def convert(line, dictionary, ignore_space = False):
    s = " " * ignore_space
    idx = [i for i, c in enumerate(line) if c != s]
    norm = line.replace(s, "")
    maxlen = max(map(len, dictionary))

    i = 0
    while i < len(norm):
        matched = list()
        for j in range(min((len(norm) - i), maxlen)):
            w = norm[i:i + j + 1]
            if w in dictionary:
                matched.append(w)
        if not matched:
            i += 1
            continue
        src = max(matched, key = len)
        tgt = dictionary[src]
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
    do = dict()
    load_dict(do, "fan2jian.tsv")
    load_dict(do, "tw2cn.tsv")
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        converted = convert(line, do, ignore_space = True)
        print(converted)
    fo.close()
