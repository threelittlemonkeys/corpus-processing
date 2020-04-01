import sys
import re

def count_chars(filename):
    fo = open(filename)
    pl = dict()
    for line in fo:
        for c in line:
            if c not in pl:
                pl[c] = 0
            pl[c] += 1
    fo.close()
    for c, f in sorted(pl.items()):
        print(c, hex(ord(c)), f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])

    count_chars(sys.argv[1])
