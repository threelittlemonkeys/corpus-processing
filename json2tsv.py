import sys
import re
import json

if len(sys.argv) not in (2, 3):
    sys.exit("Usage: %s filename (name1 ...)")

filename = sys.argv[1]
names = sys.argv[2:]

with open(filename) as fo:
    for line in fo:
        try:
            data = json.loads(line)
        except:
            continue
        if type(data) != dict:
            continue
        if not names:
            print(list(data.keys())
            break
        cols = []
        for x in names:
            y = ""
            if x in data:
                y = data[x]
            if y:
                y = y.strip()
                y = re.sub("\s+", " ", y)
            cols.append(y)
        print(*cols, sep = "\t")
