import sys
import re

if len(sys.argv) != 2:
    sys.exit("Usage: %s ref < txt" % sys.argv[0])

ref = dict()
with open(filename) as fo:
    for line in fo:
        idx, txt = line.split("\t", 1)
        if idx not in ref:
            ref[idx] = list()
        ref[idx].append(txt)

for line in sys.stdin:
    idx, _ = line.split("\t")[0]
    if idx in ref:
        for txt in ref[idx]:
            print(idx, txt, sep = "\t", end = "")
        continue
    print(line, end = "")
