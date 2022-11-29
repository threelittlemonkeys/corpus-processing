import sys
import re

if len(sys.argv) != 3:
    sys.exit("Usage: %s ref txt" % sys.argv[0])

def normalize(txt):
    return re.sub("\s+", " ", txt).strip()

ref = {}
count = 0

with open(sys.argv[1]) as fi:
    for line in fi:
        *idx, src0, tgt0, src1, tgt1 = list(map(normalize, line.split("\t")))
        k = (src0, tgt0)
        if k not in ref:
            ref[k] = []
        ref[k].append((src1, tgt1))


fo = open(sys.argv[2] + ".replaced", "w")
with open(sys.argv[2]) as fi:
    for line in fi:
        *idx, src0, tgt0 = map(normalize, line.split("\t"))
        k = (src0, tgt0)
        if k not in ref:
            print(line, end = "", file = fo)
            continue
        for (src1, tgt1) in ref[k]:
            print(*idx, src1, tgt1, sep = "\t", file = fo)
        count += 1
fo.close()

print("%d references" % len(ref), file = sys.stderr)
print("%d lines replaced" % count, file = sys.stderr)
