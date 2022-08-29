import sys
import re
from utils import *
from ibm_model1 import ibm_model1

def validate(w, lang):
    if w in ("<NULL>", "<UNK>"):
        return False
    if lang == "ja" and not re.search("[\u3040-\u309F\u4E00-\u9FFF]", w):
        return False
    if lang == "ko" and not re.search("[\uAC00-\uD7AF]", w):
        return False
    return True

def filter_phrase_table(model, threshold, outfile):

    fo = open(outfile, "w")
    cands = [[], []]

    for xi in model.vocab[0]:

        xw = model.itw[0][xi]
        if not validate(xw, model.src_lang):
            continue

        for yi in model.vocab[0][xi]:

            yw = model.itw[1][yi]
            if not validate(yw, model.tgt_lang):
                continue

            pxy = model.prob[0].get(xi, {}).get(yi, model.min_prob)
            pyx = model.prob[1].get(yi, {}).get(xi, model.min_prob)
            cand = (pxy, pyx, xw, yw)

            k = sum(cand[:2]) / 2 < threshold
            cands[k].append(cand)

    for i in range(2):
        if i:
            print(file = fo)
        for cand in sorted(cands[i], key = lambda x: -sum(x[:2])):
            print("%f\t%f\t%s\t%s" % cand, file = fo)

    fo.close()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.exit("Usage: %s model threshold" % sys.argv[0])

    filename = sys.argv[1]
    threshold = float(sys.argv[2])

    model = ibm_model1()
    model.load_vocab(re.sub("\.ibm_model1\.epoch[0-9]+$", "", filename))
    model.load_model(filename)

    filter_phrase_table(
        model = model,
        threshold = threshold,
        outfile = re.sub("\.epoch[0-9]+$", "", filename) + ".phrase_table"
    )
