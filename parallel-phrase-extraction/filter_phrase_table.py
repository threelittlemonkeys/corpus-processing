import sys
import re
from ibm_model1 import ibm_model1

def filter_phrase_table(model, threshold, outfile):

    fo = open(outfile, "w")
    itw = model.itw
    probs = model.probs
    cands = [[], []]

    for x in model.vocab[0]:
        for y in model.vocab[0][x]:
            if x <= 1 or y <= 1:
                continue
            cand = (probs[0][x][y], probs[1][y][x], itw[0][x], itw[1][y])
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
    model.load_model(filename)

    filter_phrase_table(
        model = model,
        threshold = threshold,
        outfile = re.sub("\.epoch[0-9]+$", "", filename) + ".phrase_table"
    )
