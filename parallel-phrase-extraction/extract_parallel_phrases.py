import sys
from ibm_model1 import ibm_model1

def filter_phrase_table(model, threshold, outfile):

    fo = open(outfile, "w")
    cands = [[], []]

    for x in model.vocab[0]:
        for y in model.vocab[0][x]:
            if not (x and y):
                continue
            cand = (model.probs[0][x][y], model.probs[1][y][x], x, y)
            if cand[0] < threshold or cand[1] < threshold:
                cands[1].append(cand)
                continue
            cands[0].append(cand)

    for i in range(2):
        if i:
            print(file = fo)
        for cand in sorted(cands[i], key = lambda x: -sum(x[:2])):
            print("%f\t%f\t%s\t%s" % cand, file = fo)

    fo.close()

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("Usage: %s model data threshold" % sys.argv[0])

    model_filename = sys.argv[1]
    data_filename = sys.argv[2]
    threshold = float(sys.argv[3])

    model = ibm_model1()
    model.load_model(model_filename)

    filter_phrase_table(
        model = model,
        threshold = threshold,
        outfile = f"{data_filename}.ibm_model1.phrase_table"
    )
