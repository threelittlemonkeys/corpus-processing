import sys
import re

def normalize(x):
    x = re.sub("[^0-9A-Za-z\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", x)
    x = x.lower()
    return x

def pivot_bitext(fn_src, src_idx, fn_tgt, tgt_idx):
    pool = {}
    src_idx = int(src_idx)
    tgt_idx = int(tgt_idx)

    fo = open(fn_src)
    for line in fo:
        _, *pair = line.strip().split("\t")
        if len(pair) != 2:
            continue
        src = pair[src_idx]
        pivot = normalize(pair[1 - src_idx])
        pool[pivot] = src
    fo.close()

    fo = open(fn_tgt)
    for line in fo:
        _, *pair = line.strip().split("\t")
        if len(pair) != 2:
            continue
        tgt = pair[tgt_idx]
        pivot = normalize(pair[1 - tgt_idx])
        if pivot in pool:
            print(pool[pivot], tgt, sep = "\t")
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: %s src src_idx tgt tgt_idx" % sys.argv[0])
    pivot_bitext(*sys.argv[1:])
