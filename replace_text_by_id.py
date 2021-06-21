import sys
import re

def replace_text_by_id(filename):

    pl = {}
    fo = open(filename)
    for line in fo:
        idx, txt = line.split("\t", 1)
        pl[idx] = txt
    fo.close()

    for line in sys.stdin:
        idx, *_ = line.split("\t")
        if idx in pl:
            print(idx, pl[idx], sep = "\t", end = "")
            continue
        print(idx, line, sep = "\t", end = "")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s ref < txt" % sys.argv[0])
    replace_text_by_id(*sys.argv[1:])
