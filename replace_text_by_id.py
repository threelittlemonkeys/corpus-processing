import sys
import re

def replace_text_by_id(filename):

    pl = {}
    fo = open(filename)
    for line in fo:
        idx, txt = line.split("\t", 1)
        if idx not in pl:
            pl[idx] = list()
        pl[idx].append(txt)
    fo.close()

    for line in sys.stdin:
        idx, *_ = line.split("\t")
        if idx in pl:
            for txt in pl[idx]:
                print(idx, txt, sep = "\t", end = "")
            continue
        print(line, end = "")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s ref < txt" % sys.argv[0])
    replace_text_by_id(*sys.argv[1:])
