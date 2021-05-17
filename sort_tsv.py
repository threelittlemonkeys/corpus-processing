import sys
import re

for line in sys.stdin:
    line = line.strip()
    a, *b = line.split("\t")
    b = [re.sub("\s+", " ", w.strip()) for w in b]
    print(a, *sorted(b), sep = "\t")
