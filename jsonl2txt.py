import sys
import re
import ast
import json

if len(sys.argv) < 2:
    sys.exit("Usage: %s filename (name1 ...)")

filename = sys.argv[1]
names = sys.argv[2:]

def normalize(line):
    line = re.sub("\s+", " ", line)
    line = line.strip()
    return line

def dump(obj, data, key = ""):

    if type(obj) in (int, float):
        data.append((key, txt))

    if type(obj) == str:
        for txt in obj.split("\n"):
            txt = normalize(txt)
            if txt == "":
                continue
            data.append((key, txt))

    if type(obj) == list:
        for e in obj:
            dump(e, data, key)

    if type(obj) == dict:
        for k, v in obj.items():
            dump(v, data, (key + "." if key else "") + k)

with open(filename) as fo:

    for line in fo:

        try:
            line = json.loads(line)
        except:
            line = ast.literal_eval(line)

        data = []
        dump(line, data)

        for item in data:
            k, v = item
            if names and k not in names:
                continue
            print(k, v, sep = "\t")
