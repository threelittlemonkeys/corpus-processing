import sys
import time
from utils import *
sys.path.append("../xl_tokenizer")
from tokenizer import tokenize
from sentence_transformers import SentenceTransformer

class xl_phrase_aligner():

    def __init__(self, src_lang, tgt_lang, batch_size, phrase_maxlen, threshold, verbose):
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.batch_size = batch_size
        self.phrase_maxlen = phrase_maxlen
        self.threshold = threshold
        self.verbose = verbose

        print("batch_size =", self.batch_size, file = sys.stderr)
        print("phrase_maxlen =", self.phrase_maxlen, file = sys.stderr)
        print("threshold =", self.threshold, file = sys.stderr)

        self.model = self.load_model()

    def load_model(self):
        # Language-agnostic BERT Sentence Embedding (LaBSE)
        print("loading LaBSE", file = sys.stderr)
        model = SentenceTransformer("LaBSE")
        print("loaded LaBSE", file = sys.stderr)
        return model

    def preprocess(self, batch):
        ps = []
        data = []
        for line in batch:
            *idx, x, y = line.split("\t")
            xws = tokenize(self.src_lang, x, use_tagger = True)
            yws = tokenize(self.tgt_lang, y, use_tagger = True)
            xrs, xps = zip(*phrase_iter(xws, self.phrase_maxlen))
            yrs, yps = zip(*phrase_iter(yws, self.phrase_maxlen))
            ps.extend(xps)
            ps.extend(yps)
            data.append((x, xws, xrs, xps, y, yws, yrs, yps))

        i = 0
        hs = self.model.encode(ps, batch_size = self.batch_size)
        for x, xws, xrs, xps, y, yws, yrs, yps in data:
            xhs = hs[i:i + len(xps)]
            i += len(xps)
            yhs = hs[i:i + len(yps)]
            i += len(yps)

            if self.verbose:
                print("src", x, sep = "\t")
                print("tgt", y, sep = "\t")
                print("src_tokens", xws, sep = "\t")
                print("tgt_tokens", yws, sep = "\t")
                print()

            yield xws, xrs, xps, xhs, yws, yrs, yps, yhs

    def sentence_similarity(self, batch):
        lines = []
        for line in batch:
            *idx, x, y = line.split("\t")
            lines.extend([x, y])
        hs = self.model.encode(lines, batch_size = self.batch_size)

        for i in range(0, len(hs), 2):
            yield cos_similarity(*hs[i: i + 2])

    def phrase_similarity(self, xws, xrs, xps, xhs, yws, yrs, yps, yhs):
        pss = []
        for xr, xp, xh in zip(xrs, xps, xhs):
            _pss = []
            for yr, yp, yh in zip(yrs, yps, yhs):
                ps = cos_similarity(xh, yh)
                _pss.append([ps, (xr, yr), (xp, yp)])
            if _pss:
                pss.append(max(_pss))

        if self.verbose:
            for ps, (xr, yr), (xp, yp) in pss:
                print(f"{ps:.4f} ({xr}, '{xp}'), ({yr}, '{yp}')")
            print()

        return xws, yws, pss

    def bijection(self, _xws, _yws, pss): # linear bijective alignment
        cands = []
        for w in pss:
            if len(cands) == w[1][0][0]:
                cands.append([])
            if w[0] < self.threshold:
                continue
            cands[-1].append(w)
        cands = [max(ws) for ws in cands if ws]

        score = 0
        phrases = []
        xws, yws = [*_xws], [*_yws]
        for ps, (xr, yr), _ in cands:
            if phrases and (xr[0] < phrases[-1][0][1] or yr[0] < phrases[-1][1][1]):
                continue
            tag = "%d:%.4f( " % (len(phrases), ps)
            score += (xr[1] - xr[0]) + (yr[1] - yr[0])
            phrases.append((xr, yr))
            for ws, (i, j) in zip((xws, yws), (xr, yr)):
                ws[i] = tag + ws[i]
                ws[j - 1] += " )"
        score /= len(_xws) + len(_yws)

        return " ".join(xws), " ".join(yws), score

    def extraction(self, _xws, _yws, pss):

        ops = []
        cands = []

        def compare(a, b, c, d):
            if d <= a or b <= c:
                return "DISJOINT"
            if c == a < b == d:
                return "IDENTICAL"
            if c <= a < b <= d:
                return "SUBPHRASE"
            if a <= c < d <= b:
                return "SUPERPHRASE"
            return False

        for ps, (xr, yr), _ in sorted(pss, reverse = True):
            if ps < self.threshold:
                break
            adds = []
            dels = []
            for cand in cands:
                if not cand[3]:
                    continue
                _ps, _xr, _yr, _ = cand
                _x = compare(*xr, *_xr)
                _y = compare(*yr, *_yr)
                _xy = {_x, _y}
                if _x == _y == "DISJOINT":
                    continue
                if _xy == {"SUBPHRASE", "SUPERPHRASE"}:
                    adds.append(cand)
                    continue
                if _xy.issubset({"IDENTICAL", "SUPERPHRASE"}):
                    dels.append(cand)
                    continue
                ops.append(f"{ps:.4f} ({xr}, {yr}) < {_ps:.4f} ({_xr}, {_yr})")
                break
            else:
                for cand in adds:
                    _ps, _xr, _yr, _ = cand
                    ops.append(f"{ps:.4f} ({xr}, {yr}) > {_ps:.4f} ({_xr}, {_yr})")
                    xr = (min(xr[0], _xr[0]), max(xr[1], _xr[1]))
                    yr = (min(yr[0], _yr[0]), max(yr[1], _yr[1]))
                    cand[3] = False
                for cand in dels:
                    cand[3] = False
                cands.append([ps, xr, yr, True])
        cands = [e[:-1] for e in cands if e[-1]]

        score = 0
        xws, yws = [*_xws], [*_yws]
        for idx, (ps, xr, yr) in enumerate(sorted(cands, key = lambda x: x[1])):
            tag = "%d:%.4f( " % (idx, ps)
            score += (xr[1] - xr[0]) + (yr[1] - yr[0])
            for ws, (i, j) in zip((xws, yws), (xr, yr)):
                ws[i] = tag + ws[i]
                ws[j - 1] += " )"
        score /= len(_xws) + len(_yws)

        return " ".join(xws), " ".join(yws), score

    def align(self, batch, method):
        data_iter = self.preprocess(batch)
        for data in data_iter:
            yield getattr(self, method)(*self.phrase_similarity(*data))

if __name__ == "__main__":

    if len(sys.argv) not in (5, 6):
        sys.exit("Usage: %s src_lang tgt_lang sentence|bijection|extraction bitext [-v]" % sys.argv[0])

    aligner = xl_phrase_aligner(
        src_lang = sys.argv[1],
        tgt_lang = sys.argv[2],
        batch_size = 1024,
        phrase_maxlen = 5,
        threshold = 0.7,
        verbose = (len(sys.argv) == 6 and sys.argv[5] == "-v")
    )

    ln = 0
    batch = []
    timer = time.time()
    method = sys.argv[3]
    fo = open(sys.argv[4])

    while True:
        ln += 1
        line = fo.readline().strip()

        if line:
            batch.append(line)
            if len(batch) < aligner.batch_size:
                continue
        elif not batch:
            break

        if method == "sentence":
            sent_scores = aligner.sentence_similarity(batch)
            for line, score in zip(batch, sent_scores):
                print(score, line, sep = " \t")

        if method in ("bijection", "extraction"):
            algn_scores = aligner.align(batch, method)
            for line, algn_score in zip(batch, algn_scores):
                src_algn, tgt_algn, algn_score = algn_score
                print(line)
                print(f"src_aligned\t{src_algn}")
                print(f"tgt_aligned\t{tgt_algn}")
                print(f"alignment_score\t{algn_score:f}")
                (input if aligner.verbose else print)()

        batch.clear()

        print("%d lines (%.f seconds)" % (ln, time.time() - timer), file = sys.stderr)
        timer = time.time()

    fo.close()
