import sys
import re

def normalize(txt):
    txt = txt.lower()
    return txt

def tokenize(txt):
    txt = re.sub("(?<=[^ ])(?=[^ 0-9A-Za-z])", r" ", txt)
    txt = re.sub("(?<=[^ 0-9A-Za-z])(?=[^ ])", r" ", txt)
    return txt

def corpus_filter(src_lang, tgt_lang, filename):
    fo = open(filename)

    for line in fo:
        line = line.strip()
        src, tgt = line.split("\t")
        src = tokenize(normalize(src))
        tgt = tokenize(normalize(tgt))

    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang filename" % sys.argv[0])

    corpus_filter(*sys.argv[1:])
