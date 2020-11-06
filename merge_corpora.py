import sys

with open(sys.argv[1]) as fo:
    ls = fo.read().strip().split("\n")

for cid, filename in enumerate(ls):
    fo = open(filename)
    for sid, sent in enumerate(fo):
        print("%d.%d\t%s" % (cid, sid, sent), end = "")
    fo.close()
