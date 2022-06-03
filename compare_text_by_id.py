import sys
import re

def compare_text_by_id(action, filename):

    pl = dict()
    with open(filename) as fo:
        for line in fo:
            idx = line.split("\t")[0]
            pl[idx] = True

    for line in sys.stdin:
        idx, *_ = line.split("\t")
        if action == "dup" and idx in pl:
            print(line, end = "")
        if action == "uniq" and idx not in pl:
            print(line, end = "")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("dup", "uniq"):
        sys.exit("Usage: %s dup|uniq ref < txt" % sys.argv[0])
    compare_text_by_id(*sys.argv[1:])
