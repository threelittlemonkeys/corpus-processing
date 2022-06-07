import sys
import re

if len(sys.argv) != 2:
    sys.exit("Usage: %s ref < txt" % sys.argv[0])

ref = dict()
with open(sys.argv[1]) as fo:
    for line in fo:
        idx, txt = line.split("\t", 1)
        if idx not in ref:
            ref[idx] = list()
        ref[idx].append(txt)

for line in sys.stdin:
    idx = line.split("\t")[0]
    if idx in ref:
        for txt in ref[idx]:
            print(line, end = "", file = sys.stderr)
            print(idx, txt, sep = "\t", end = "", file = sys.stderr)
            print(idx, txt, sep = "\t", end = "", file = sys.stdout)
            print(file = sys.stderr)
        continue
    print(line, end = "", file = sys.stdout)
