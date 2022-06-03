import sys
import re

if len(sys.argv) != 2:
    sys.exit("Usage: %s ref < txt" % sys.argv[0])

ref = set()
with open(filename) as fo:
    for line in fo:
        idx = line.strip()
        ref.add(idx)

for line in sys.stdin:
    idx = line.split("\t")[0]
    if idx in ref:
        continue
    print(line, end = "")
