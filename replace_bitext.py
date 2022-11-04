import sys
import re

if len(sys.argv) != 3:
    sys.exit("Usage: %s ref txt" % sys.argv[0])

def normalize(txt):
    return re.sub("[^A-Za-z0-9\u3040-\u30FF\u4E00-\u9FFF\uAC00-\uD7AF]", "", txt)
    return re.sub("\s+", " ", txt).strip()

ref = {}
count = 0

with open(sys.argv[1]) as f:
    for line in f:
        *idx, src0, tgt0, src1, tgt1 = map(normalize, line.split("\t"))
        k = (src0, tgt0)
        if k not in ref:
            ref[k] = []
        ref[k].append((src1, tgt1))

fi = open(sys.argv[2])
fo = open(sys.argv[2] + ".replaced", "w")

for line in fi:
    *idx, src0, tgt0 = map(normalize, line.split("\t"))
    k = (src0, tgt0)

    if k not in ref:
        print(line, end = "", file = fo)
        continue

    for (src1, tgt1) in ref[k]:
        print(*idx, src1, tgt1, sep = "\t", file = fo)

    count += 1

print("%d references" % len(ref))
print("%d lines replaced" % count)

fi.close()
fo.close()
