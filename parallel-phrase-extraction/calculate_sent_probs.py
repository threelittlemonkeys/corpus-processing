import sys
from ibm_model1 import ibm_model1
from utils import tokenize

def calculate_sent_probs(model, infile, outfile):

    cands = []
    fin = open(infile)
    fout = open(outfile, "w")

    for ln, line in enumerate(fin, 1):
        x, y = line.split("\t")
        xs = [model.wti[0][x] for x in tokenize(model.src_lang, x)]
        ys = [model.wti[1][y] for y in tokenize(model.tgt_lang, y)]

        model.dir = 0
        f_prob = model.sent_prob(xs, ys)
        model.dir = 1
        b_prob = model.sent_prob(ys, xs)

        cands.append((f_prob, b_prob, line))

    for cand in sorted(cands, key = lambda x: -sum(x[:2])):
        print(*cand, sep = "\t", end = "", file = fout)

    fin.close()
    fout.close()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.exit("Usage: %s model data" % sys.argv[0])

    model_filename = sys.argv[1]
    data_filename = sys.argv[2]

    model = ibm_model1()
    model.load_model(model_filename)

    calculate_sent_probs(
        model = model,
        infile = data_filename,
        outfile = f"{data_filename}.ibm_model1.sent_probs"
    )
