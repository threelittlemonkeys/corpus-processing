import sys
import re
import time
from utils import *
from sentence_transformers import SentenceTransformer

# suppress InsecureRequestWarning
import requests
requests.packages.urllib3.disable_warnings()

class phrase_aligner():

    def __init__(self, src_lang, tgt_lang, batch_size, phrase_maxlen, threshold, verbose):

        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.batch_size = batch_size
        self.phrase_maxlen = phrase_maxlen
        self.threshold = threshold
        self.verbose = verbose

        print(f"src_lang = {src_lang}", file = sys.stderr)
        print(f"tgt_lang = {tgt_lang}", file = sys.stderr)
        print(f"batch_size = {batch_size}", file = sys.stderr)
        print(f"phrase_maxlen = {phrase_maxlen}", file = sys.stderr)
        print(f"threshold = {self.threshold}", file = sys.stderr)

        self.model = self.load_model()

    def load_model(self):

        # Language-agnostic BERT Sentence Embedding (LaBSE)
        print("loading LaBSE", file = sys.stderr)
        model = SentenceTransformer("sentence-transformers/LaBSE")
        print("loaded LaBSE", file = sys.stderr)

        # if requests.exceptions.SSLError occurs:
        # add kwargs["verify"] = False
        # in def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        # in class UniqueRequestIdAdapter(HTTPAdapter):
        # in /lib/python/site-packages/huggingface_hub/utils/_http.py

        return model

    def preprocess(self, batch):

        ps = []
        data = []

        for line in batch:

            x, y = line.split("\t")
            xws = re.sub("\\s+", " ", x).strip().split(" ")
            yws = re.sub("\\s+", " ", y).strip().split(" ")
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
                print(f"src_text\t{x}")
                print(f"tgt_text\t{y}")
                print(f"src_tokens\t{xws}")
                print(f"tgt_tokens\t{yws}")
                print()

            yield xws, xrs, xps, xhs, yws, yrs, yps, yhs

    def sentence_similarity(self, batch):

        lines = []
        for line in batch:
            x, y = line.split("\t")
            lines.extend([x, y])
        hs = self.model.encode(lines, batch_size = self.batch_size)

        for i in range(0, len(hs), 2):
            yield cos_similarity(*hs[i: i + 2])

    def phrase_similarity(self, xws, xrs, xps, xhs, yws, yrs, yps, yhs):

        xys = []

        for xr, xp, xh in zip(xrs, xps, xhs):

            _xys = []

            for yr, yp, yh in zip(yrs, yps, yhs):
                sim = cos_similarity(xh, yh)
                _xys.append([sim, (xr, yr), (xp, yp)])

            if _xys:
                xys.append(max(_xys))

        if self.verbose:
            for sim, (xr, yr), (xp, yp) in xys:
                print(f"{sim:.4f} {(xr, xp)} {(yr, yp)}")
            print()

        return xws, yws, xys

    def bijection(self, _xws, _yws, xys): # linear bijective alignment

        cands = [[] for _ in _xws]

        for xy in xys:
            if xy[0] < self.threshold:
                continue
            cands[xy[1][0][0]].append(xy)

        cands = [max(xys) for xys in cands if xys]

        xws, yws, lens = [*_xws], [*_yws], [0, 0]
        phrase_scores = []
        sentence_score = 0

        for sim, (xr, yr), _ in cands:

            if xr[0] < lens[0] or yr[0] < lens[1]: # phrase collision
                continue

            tag = f"({len(phrase_scores)}: "
            lens = [xr[1], yr[1]]
            phrase_scores.append(sim)
            sentence_score += (xr[1] - xr[0]) + (yr[1] - yr[0])

            for ws, (i, j) in zip((xws, yws), (xr, yr)):
                ws[i] = tag + ws[i]
                ws[j - 1] += " )"

        sentence_score /= len(_xws) + len(_yws)

        return " ".join(xws), " ".join(yws), phrase_scores, sentence_score

    def extraction(self, _xws, _yws, xys): # non-linear alignment

        ops = []
        cands = []

        def _compare(a, b, c, d):
            if d <= a or b <= c:
                return "DISJOINT"
            if c == a < b == d:
                return "IDENTICAL"
            if c <= a < b <= d:
                return "SUBPHRASE"
            if a <= c < d <= b:
                return "SUPERPHRASE"
            return False

        for sim, (xr, yr), _ in sorted(xys, reverse = True):

            if sim < self.threshold:
                break

            additions = []
            deletions = []

            for cand in cands:

                _sim, _xr, _yr, _state = cand

                if not _state:
                    continue

                _a = _compare(*xr, *_xr)
                _b = _compare(*yr, *_yr)
                _ab = {_a, _b}

                if _a == _b == "DISJOINT":
                    continue
                if _ab == {"SUBPHRASE", "SUPERPHRASE"}:
                    additions.append(cand)
                    continue
                if _ab.issubset({"IDENTICAL", "SUPERPHRASE"}):
                    deletions.append(cand)
                    continue

                ops.append(f"{sim:.4f} ({xr}, {yr}) < {_sim:.4f} ({_xr}, {_yr})")
                break
            else:
                for cand in additions:
                    _sim, _xr, _yr, _ = cand
                    ops.append(f"{sim:.4f} ({xr}, {yr}) > {_sim:.4f} ({_xr}, {_yr})")
                    xr = (min(xr[0], _xr[0]), max(xr[1], _xr[1]))
                    yr = (min(yr[0], _yr[0]), max(yr[1], _yr[1]))
                    cand[3] = False
                for cand in deletions:
                    cand[3] = False
                cands.append([sim, xr, yr, True])

        cands = [cand[:-1] for cand in cands if cand[-1]]

        xws, yws = [*_xws], [*_yws]
        phrase_scores = []
        sentence_score = 0

        for idx, (sim, xr, yr) in enumerate(sorted(cands, key = lambda x: x[1])):
            tag = f"({idx}: "
            phrase_scores.append(sim)
            sentence_score += (xr[1] - xr[0]) + (yr[1] - yr[0])
            for ws, (i, j) in zip((xws, yws), (xr, yr)):
                ws[i] = tag + ws[i]
                ws[j - 1] += " )"

        sentence_score /= len(_xws) + len(_yws)

        return " ".join(xws), " ".join(yws), phrase_scores, sentence_score

    def align(self, batch, method):
        data_iter = self.preprocess(batch)
        for data in data_iter:
            yield getattr(self, method)(*self.phrase_similarity(*data))

if __name__ == "__main__":

    if len(sys.argv) not in (5, 6):
        sys.exit("Usage: %s src_lang tgt_lang sentence|bijection|extraction tokenized_bitext [-v]" % sys.argv[0])

    src_lang, tgt_lang, method, filename = sys.argv[1:5]

    aligner = phrase_aligner(
        src_lang = src_lang,
        tgt_lang = tgt_lang,
        batch_size = 1024,
        phrase_maxlen = 5,
        threshold = 0.7,
        verbose = (len(sys.argv) == 6 and sys.argv[5] == "-v")
    )

    data_size = 0
    timer = time.time()

    for batch in batch_iter(filename, aligner.batch_size):

        data_size += len(batch)

        if method == "sentence":

            sentence_scores = aligner.sentence_similarity(batch)
            for line, sentence_score in zip(batch, sentence_scores):
                print(sentence_score, line, sep = " \t")

        if method in ("bijection", "extraction"):

            alignments = aligner.align(batch, method)
            for line, alignment in zip(batch, alignments):
                src_aligned, tgt_aligned, phrase_scores, sentence_score = alignment
                print(f"src_aligned\t{src_aligned}")
                print(f"tgt_aligned\t{tgt_aligned}")
                print("phrase_scores", phrase_scores, sep = "\t")
                print("sentence_score", sentence_score, sep = "\t")
                (input if aligner.verbose else print)()

    print("%d lines (%.f seconds)" % (data_size, time.time() - timer), file = sys.stderr)
    timer = time.time()
