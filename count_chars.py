import sys
import re

pl = {}
for line in sys.stdin:
    for c in line:
        if c not in pl:
            pl[c] = 0
        pl[c] += 1

for c, f in sorted(pl.items()):
    print(c, hex(ord(c)), f)
