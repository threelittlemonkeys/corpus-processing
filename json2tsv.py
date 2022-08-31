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
            print(list(data.keys()))
            break

        cols = []
        for k in names:
            v = data[k] if k in data else ""

            if type(v) == str:
                v = re.sub("\s+", " ", v).strip()

            if type(v) == list:
                v = [re.sub("\s+", " ", x).strip() for x in v]

            cols.append(v)
        print(*cols, sep = "\t")
