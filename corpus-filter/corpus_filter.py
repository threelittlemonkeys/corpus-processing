import sys
import re

ERROR_CODE = [
    "SRC:EMPTY", # empty source sentence
    "TGT:EMPTY", # empty target sentence
    "IDENTICAL", # identical source and target sentences
    "SRC:TOO_SHORT", # source sentence too short
    "TGT:TOO_SHORT", # target sentence too short
    "SRC:TOO_LONG", # source sentence too long
    "TGT:TOO_LONG", # target sentence too long
]

MINIMUM_SENTENCE_LENGTH = 2
SENTENCE_LENGTH_RATIO = 3

def normalize(txt):
    txt = txt.lower()
    return txt

def tokenize(txt):
    txt = re.sub("(?<=[^ ])(?=[^ 0-9A-Za-z])", r" ", txt)
    txt = re.sub("(?<=[^ 0-9A-Za-z])(?=[^ ])", r" ", txt)
    txt = txt.split(" ")
    return txt

def log_error(errors, error_counts, i):
    k = ERROR_CODE[i]
    errors.append(k)
    error_counts[k] += 1

def corpus_filter(src_lang, tgt_lang, filename):
    ln = 0
    fo = open(filename)
    error_counts = {k: 0 for k in ERROR_CODE}

    for line in fo:
        line = line.strip()
        errors = list()

        _src, _tgt = line.split("\t")
        src = normalize(_src)
        tgt = normalize(_tgt)

        if src == "":
            log_error(errors, error_counts, 0)
        if tgt == "":
            log_error(errors, error_counts, 1)
        if src == tgt:
            log_error(errors, error_counts, 2)

        src = tokenize(src)
        tgt = tokenize(tgt)

        if len(src) < MINIMUM_SENTENCE_LENGTH:
            log_error(errors, error_counts, 3)
        if len(tgt) < MINIMUM_SENTENCE_LENGTH:
            log_error(errors, error_counts, 4)

        if len(src) / len(tgt) > SENTENCE_LENGTH_RATIO:
            log_error(errors, error_counts, 5)
        if len(tgt) / len(src) > SENTENCE_LENGTH_RATIO:
            log_error(errors, error_counts, 6)

        if len(errors):
            print(_src, _tgt, ",".join(errors), sep = "\t")
        ln += 1

    fo.close()

    print()
    for k, v in sorted(error_counts.items(), key = lambda x: -x[1]):
        print(k, v, "(%.4f%%)" % (v / ln * 100))
    print("%d sentences in total" %  ln)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang filename" % sys.argv[0])

    corpus_filter(*sys.argv[1:])
