import sys
import re
import math
sys.path.append("../xl_tokenizer")
from tokenizer import tokenize
from collections import defaultdict

def extract_parallel_phrases(src_lang, tgt_lang, filename, min_freq):

    x_count = defaultdict(int)
    y_count = defaultdict(int)
    xy_count = defaultdict(lambda: defaultdict(int))
    scores = defaultdict(lambda: defaultdict(float))

    print("calculating word frequencies", file = sys.stderr)

    fo = open(filename)
    for ln, line in enumerate(fo, 1):
        *idx, x, y = line.split("\t")

        xws = set(tokenize(src_lang, x, alnum_only = True))
        yws = set(tokenize(tgt_lang, y, alnum_only = True))

        for xw in xws:
            if len(xw) == 1:
                continue
            x_count[xw] += 1
            for yw in yws:
                xy_count[xw][yw] += 1

        for yw in yws:
            y_count[yw] += 1

        if ln % 100000 == 0:
            print(ln, "lines", file = sys.stderr)

    print("calculating scores", file = sys.stderr)

    for xw, yws in sorted(xy_count.items(), key = lambda x: -x_count[x[0]]):
        if x_count[xw] < min_freq:
            break
        for yw in yws:
            if xy_count[xw][yw] < max(x_count[xw] * 0.1, min_freq):
                continue
            scores[xw][yw] = math.log(xy_count[xw][yw]) - math.log(y_count[yw])

    fo.close()

    for xw, yws in scores.items():
        print(xw, x_count[xw], *sorted(yws.items(), key = lambda x: -x[1]))

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang filename" % sys.argv[0])

    src_lang = sys.argv[1]
    tgt_lang = sys.argv[2]
    filename = sys.argv[3]
    min_freq = 3

    extract_parallel_phrases(src_lang, tgt_lang, filename, min_freq)
