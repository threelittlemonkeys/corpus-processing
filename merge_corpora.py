import sys

with open(sys.argv[1]) as fo:
    ls = fo.read().strip().split("\n")

pl = dict()
for idx, filename in enumerate(ls):
    fo = open(filename)
    for line in fo:
        line = line.strip()
        if line in pl:
            continue
        pl[line] = True
        print(idx, line, sep = "\t")
    fo.close()
