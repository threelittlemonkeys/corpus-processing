import sys
import re

seq = []
for line in sys.stdin:
    if line == "EOS\n":
        print(" ".join(seq))
        seq = []
        continue
    m = re.match("(.+?)\t(.+?),", line)
    word = m.group(1).strip()
    tag = m.group(2).strip()
    seq.append("%s/%s" % (word, tag))
