import sys
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

def detokenize(x):
    x = x.replace(" ", "")
    x = x.replace("＃", " ")
    x = x.strip()
    return x

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit("Usage: %s src refs hyps" % sys.argv[0])
    func = SmoothingFunction()
    src = open(sys.argv[1])
    refs = open(sys.argv[2])
    hyps = [open(x) for x in sys.argv[3:]]
    scores = [[] for _ in hyps]
    for s, r, *hs in zip(src, refs, *hyps):
        line = list()
        s = s.strip()
        _r = [r.strip().split(" ")]
        line.extend([s, detokenize(r)])
        for i, h in enumerate(hs):
            _h = h.strip().split(" ")
            b = sentence_bleu(_r, _h, smoothing_function = func.method3)
            scores[i].append(b)
            line.extend(["%0.4f" % b, detokenize(h)])
        print(*line, sep = "\t")
    refs.close()
    hyps = [x.close() for x in hyps]
    print("\t", end = "")
    for bs in scores:
        print("%0.4f\t" % (sum(bs) / len(bs)), end = "")
    print()
