import sys

with open(sys.argv[1]) as fo:
    ls = fo.read().strip().split("\n")

ls = [open(filename, "w") for filename in ls]

fo = open(sys.argv[2])
for line in fo:
    idx, line = line.split("\t", 1)
    idx = int(idx.split(".")[0])
    ls[idx].write(line)
fo.close()

for fo in ls:
    fo.close()
