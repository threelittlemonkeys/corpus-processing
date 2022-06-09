import sys
import re
import json

if len(sys.argv) < 3:
    sys.exit("Usage: %s filename name1 ...")

filename = sys.argv[1]
names = sys.argv[2:]

with open(filename) as fo:
    for line in fo:
        try:
            jo = json.loads(line)
        except:
            continue
        if type(jo) != dict:
            continue
        tsv = []
        for x in names:
            y = ""
            if x in jo:
                y = jo[x]
            if y:
                y = y.strip()
                y = re.sub("\s+", " ", y)
            tsv.append(y)
        print(*tsv, sep = "\t")
