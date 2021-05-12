import sys
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: %s refs < hyps" % sys.argv[0])
    scores = list()
    func = SmoothingFunction()
    refs = open(sys.argv[1])
    hyps = sys.stdin
    for r, h in zip(refs, hyps):
        r = [r.strip().split(" ")]
        h = h.strip().split(" ")
        score = sentence_bleu(r, h, smoothing_function = func.method3)
        print("%f" % score, " ".join(r[0]), " ".join(h), sep = "\t")
        scores.append(score)
    refs.close()
    print("%f" % (sum(scores) / len(scores)))
