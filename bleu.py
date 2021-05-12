import sys
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

def detokenize(x):
    x = x.replace(" ", "")
    x = x.replace("＃", " ")
    x = x.strip()
    return x

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: %s refs hyps" % sys.argv[0])
    func = SmoothingFunction()
    refs = open(sys.argv[1])
    hyps = [open(x) for x in sys.argv[2:]]
    scores = [[] for _ in hyps]
    for r, *hs in zip(refs, *hyps):
        _r = [r.strip().split(" ")]
        print(detokenize(r), end = "")
        for i, h in enumerate(hs):
            _h = h.strip().split(" ")
            b = sentence_bleu(_r, _h, smoothing_function = func.method3)
            print("\t%f\t%s" % (b, detokenize(h)), end = "")
            scores[i].append(b)
        print()
    refs.close()
    hyps = [x.close() for x in hyps]
    print("\t", end = "")
    for bs in scores:
        print("%f\t" % (sum(bs) / len(bs)), end = "")
    print()
