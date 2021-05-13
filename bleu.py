import sys
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

def detokenize(x):
    return "".join(x).replace("＃", " ")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit("Usage: %s src refs hyps" % sys.argv[0])
    fo_src = open(sys.argv[1])
    fo_refs = open(sys.argv[2])
    fo_hyps = [open(x) for x in sys.argv[3:]]
    func = SmoothingFunction()
    scores = [[] for _ in fo_hyps]
    for src, ref, *hyps in zip(fo_src, fo_refs, *fo_hyps):
        src = [src.strip()]
        ref = ref.strip().split(" ")
        line = [*src, detokenize(ref)]
        ref = [ref]
        for i, hyp in enumerate(hyps):
            hyp = hyp.strip().split(" ")
            score = sentence_bleu(ref, hyp, smoothing_function = func.method3)
            scores[i].append(score)
            line.extend(["%0.4f" % score, detokenize(hyp)])
        if line[2] > line[4]:
            print(*line[1:], sep = "\t")
    fo_src.close()
    fo_refs.close()
    fo_hyps = [x.close() for x in fo_hyps]
    print("\t", end = "")
    for x in scores:
        print("%0.4f\t" % (sum(x) / len(x)), end = "")
    print()
