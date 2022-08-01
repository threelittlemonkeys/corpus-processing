import sys
from ibm_model1 import ibm_model1

def extract_parallel_phrases(src_lang, tgt_lang, filename, num_epochs, threshold):

    print("calculating lexical translation probabilities

    model = ibm_model1(
        src_lang = src_lang,
        tgt_lang = tgt_lang,
    )

    model.load_data(filename)
    model.train("forward", num_epochs)
    model.train("backward", num_epochs)

    fo = open("%s.phrase_table" % filename, "w")
    cands = []

    for x in model.vocab[0]:
        for y in model.vocab[0][x]:
            if not (x and y):
                continue
            if model.probs[0][x][y] < threshold:
                continue
            if model.probs[1][y][x] < threshold:
                continue
            cands.append((model.probs[0][x][y], model.probs[1][y][x], x, y))

    for cand in sorted(cands, key = lambda x: -sum(x[:2]) / 2):
        print(*cand, sep = "\t", file = fo)

    fo.close()

if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.exit("Usage: %s L1 L2 corpus num_epochs" % sys.argv[0])

    extract_parallel_phrases(
        src_lang = sys.argv[1],
        tgt_lang = sys.argv[2],
        filename = sys.argv[3],
        num_epochs = int(sys.argv[4]),
        threshold = 0.7
    )
