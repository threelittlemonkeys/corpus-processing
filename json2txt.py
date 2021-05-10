import sys
import re
import json

pool = dict()
RE_AL = re.compile("[A-Za-z\uAC00-\uD7AF]")

def normalize(line):
    line = re.sub("\s+", " ", line)
    line = line.strip()
    return line

def dump(obj):

    if type(obj) in (int, float):
        print(obj)
        return

    if type(obj) == str:
        for line in obj.split("\n"):
            line = normalize(line)
            if line == "":
                continue
            if not RE_AL.search(line):
                continue
            if line in pool:
                continue
            pool[line] = True
            print(line)
        return

    if type(obj) == list:
        for x in obj:
            dump(x)
        return

    if type(obj) == dict:
        for a, b in obj.items():
            dump(b)
        return

with open(sys.argv[1]) as fo:
    for line in fo:
        line = json.loads(line)
        dump(line)
