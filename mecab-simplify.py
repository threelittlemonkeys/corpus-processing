import sys
import re

def mecab_simplify(filename):
    seq = []
    fo = open(filename)
    for line in fo:
        if line == "EOS\n":
            print(" ".join(seq))
            seq = []
            continue
        m = re.match("(.+?)\t(.+?),", line)
        word = m.group(1).strip()
        tag = m.group(2).strip()
        seq.append("%s/%s" % (word, tag))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s filename" % sys.argv[0])
    mecab_simplify(sys.argv[1])
