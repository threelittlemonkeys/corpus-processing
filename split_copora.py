import sys


def split_corpora(fn_idx, fn_txt):
    with open(fn_idx) as fo:
        ls = fo.read().strip().split("\n")

    ls = [open(filename, "w") for filename in ls]

    fo = open(fn_txt)
    for line in fo:
        idx, line = line.split("\t", 1)
        idx = int(idx.split(".")[0])
        ls[idx].write(line)
    fo.close()

    for fo in ls:
        fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s idx txt" % sys.argv[0])
    split_corpora(*sys.argv[1:])

