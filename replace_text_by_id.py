import sys
import re

def replace_text_by_id(filename):

    ref = dict()
    fo = open(filename)
    for line in fo:
        idx, txt = line.split("\t", 1)
        if idx not in ref:
            ref[idx] = list()
        ref[idx].append(txt)
    fo.close()

    for line in sys.stdin:
        idx, *_ = line.split("\t")
        if idx in ref:
            for txt in ref[idx]:
                print(idx, txt, sep = "\t", end = "")
            continue
        print(line, end = "")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s ref < txt" % sys.argv[0])
    replace_text_by_id(*sys.argv[1:])
