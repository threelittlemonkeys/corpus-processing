import sys
import re

def delete_text_by_id(filename):

    ref = dict()
    fo = open(filename)
    for line in fo:
        idx = line.strip()
        ref[idx] = True
    fo.close()

    for line in sys.stdin:
        idx, _ = line.split("\t", 1)
        if idx in ref:
            continue
        print(line, end = "")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s ref < txt" % sys.argv[0])
    delete_text_by_id(*sys.argv[1:])
