import sys
import re
sys.path.append("../xl_tokenizer")
from xl_tokenizer import xl_tokenizer

def update_vocab(xs, ys):
    for d in range(2):
        if d:
            xs, ys = ys, xs
        for x in ["<NULL>", *xs]:
            if x not in model.counts[d]:
                counts[d][x] = 0
            counts[d][x] += 1

def prune(model, min_freq):
    for d in range(2):
        _vocab = {}
        for x in model.vocab[d]:
            if model.counts[d][x] < min_freq:
                continue
            _vocab[x] = {
                y for y in model.vocab[d][x]
                if model.counts[1 - d][y] > min_freq
            }
        model.vocab[d] = _vocab

def load_data(src_lang, tgt_lang, filename, min_freq):

    print("src_lang =", src_lang)
    print("tgt_lang =", tgt_lang)
    print("min_freq =", min_freq)
    print("loading data")

    data = []
    vocab = [{}, {}]

    fo = open(filename)
    for ln, line in enumerate(fo, 1):
        try:
            *_, x, y = line.split("\t")
        except:
            print("Error: invalid format at line %d" % ln)
            print(line, end = "")
            continue
        xs = tokenizer.tokenize(src_lang, x)
        ys = tokenizer.tokenize(tgt_lang, y)
        data.append((xs, ys))
        for d in range(2):
            for w in (xs, ys)[d]:
                if w not in vocab[d]:
                    vocab[d][w] = 0
                vocab[d][w] += 1
    fo.close()

    for i in range(2):
        vocab[i] = {w: i for i, w in enumerate(
            ["<NULL>", "<UNK>"]
            + sorted({w for w in vocab[i] if vocab[i][w] >= min_freq},
            key = lambda x: -vocab[i][x])
        )}

    data = [(
        [vocab[0][x if x in vocab[0] else "<UNK>"] for x in xs],
        [vocab[1][y if y in vocab[1] else "<UNK>"] for y in ys]
        ) for xs, ys in data
    ]

    print("data_size =", len(data))
    print("src_vocab_size =", len(vocab[0]))
    print("tgt_vocab_size =", len(vocab[1]))

    return data, vocab

def save_data(data, vocab, filename):

    fo = open(filename + ".src_vocab", "w")
    for w in vocab[0]:
        print(w, file = fo)
    fo.close()

    fo = open(filename + ".tgt_vocab", "w")
    for w in vocab[1]:
        print(w, file = fo)
    fo.close()

    fo = open(filename + ".csv", "w")
    for xs, ys in data:
        print(" ".join(map(str, xs)) + "\t" + " ".join(map(str, ys)), file = fo)

    print("saved data")
    fo.close()

if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.exit("Usage: %s src_lang tgt_lang data min_freq" % sys.argv[0])

    tokenizer = xl_tokenizer()

    data, vocab = load_data(*sys.argv[1:4], int(sys.argv[4]))
    save_data(data, vocab, sys.argv[3])
