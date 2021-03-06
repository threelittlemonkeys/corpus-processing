import sys
import re
import ast
import json

def flatten(x, y):
    for k, v in x.items():
        if type(v) == str:
            y[k] = v
        if type(v) == dict:
            flatten(v, y)

def json2tsv():
    cnt = 0
    pl = dict()
    with open(sys.argv[1]) as fo:
        names = sys.argv[2:]
        for line in fo:
            o = dict()
            vs = []
            cnt += 1
            try:
                line = json.loads(line)
            except:
                line = ast.literal_eval(line)
            flatten(line, o)
            for k in names:
                if k in o:
                    v = o[k]
                    v = re.sub("\s+", " ", v)
                    v = v.strip()
                else:
                    v = ""
                vs.append(v)
            vs = "\t".join(vs)
            if vs in pl:
                continue
            pl[vs] = True
            print(vs)

    print("%d in total" % cnt, file = sys.stderr)
    print("%d uniq" % len(pl), file = sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: %s filename name1 ...")
    json2tsv()
