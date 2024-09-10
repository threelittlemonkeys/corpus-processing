import sys
import re
import time
from utils import *
from sentence_transformers import SentenceTransformer

# suppress InsecureRequestWarning
import requests
requests.packages.urllib3.disable_warnings()

class phrase_aligner():

    def __init__(self, src_lang, tgt_lang, batch_size, window_size, thresholds, verbose):

        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.batch_size = batch_size
        self.window_size = window_size
        self.alignment_score_threshold = thresholds[0]
        self.phrase_score_threshold = thresholds[1]
        self.verbose = verbose

        print(f"src_lang = {src_lang}", file = sys.stderr)
        print(f"tgt_lang = {tgt_lang}", file = sys.stderr)
        print(f"batch_size = {batch_size}", file = sys.stderr)
        print(f"window_size = {window_size}", file = sys.stderr)
        print(f"alignment_score_threshold = {self.alignment_score_threshold}", file = sys.stderr)
        print(f"phrase_score_threshold = {self.phrase_score_threshold}", file = sys.stderr)

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

    def data_iter(self, batch):

        ps = []
        data = []

        for line in batch:

            x, y = line.split("\t")
            xws = re.sub("\\s+", " ", x).strip().split(" ")
            yws = re.sub("\\s+", " ", y).strip().split(" ")
            xrs, xps = zip(*phrase_iter(xws, self.window_size))
            yrs, yps = zip(*phrase_iter(yws, self.window_size))
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
                print(f"\nsrc_text\t{x}")
                print(f"tgt_text\t{y}")
                print(f"src_tokens\t{xws}")
                print(f"tgt_tokens\t{yws}\n")

            yield xws, xrs, xps, xhs, yws, yrs, yps, yhs

    def sentence_similarity(self, batch):

        sents = []

        for line in batch:
            x, y = line.split("\t")
            sents.extend([x, y])

        hs = self.model.encode(sents, batch_size = self.batch_size)

        for i in range(0, len(hs), 2):
            yield cosine_similarity(*hs[i: i + 2])

    def score(self, xws, xrs, xps, xhs, yws, yrs, yps, yhs):

        xys = []
        Wa = np.zeros((len(xws), len(yws)))

        for xr, xp, xh in zip(xrs, xps, xhs):
            for yr, yp, yh in zip(yrs, yps, yhs):
                xy = (cosine_similarity(xh, yh), (xr, yr), (xp, yp))
                if xy[0] < self.phrase_score_threshold:
                    continue
                xys.append(xy)
                Wa[xr[0]:xr[1], yr[0]:yr[1]] += xy[0]

        Wa_xy = normalize(Wa, axis = 1, method = "softmax")
        Wa_yx = normalize(Wa, axis = 0, method = "softmax")
        Wa = Wa_xy * Wa_yx

        if self.verbose:

            print("alignment_map =")
            print([[round(y, 4) for y in ys] for ys in Wa])
            print()

            print("alignment_scores =")
            for i in range(Wa.shape[0]):
                for j in range(Wa.shape[1]):
                    if Wa[i][j] < self.alignment_score_threshold:
                        continue
                    print(f"{Wa[i][j]:.4f} {(i, j)} {(xws[i], yws[j])}")
            print()

        for k in range(len(xys)):
            phrase_score, (xr, yr), (xp, yp) = xys[k][:3]
            alignment_score = 0
            for i in range(xr[0], xr[1]):
                for j in range(yr[0], yr[1]):
                    a = Wa[i][j]
                    if a < alignment_score:
                        continue
                    if a < self.alignment_score_threshold:
                        continue
                    alignment_score = a
                    break
                else:
                    continue
                break
            alignment_score = (alignment_score > 0)
            xys[k] = ((alignment_score, phrase_score), *xys[k][1:3])

        if self.verbose:
            print("phrase_scores =")
            for xy in xys:
                (alignment_score, phrase_score), (xr, yr), (xp, yp) = xy
                if alignment_score < self.alignment_score_threshold:
                    continue
                if phrase_score < self.phrase_score_threshold:
                    continue
                print(f"{phrase_score:.4f} {(xr, xp)} {(yr, yp)}")
            print()

        return xws, yws, xys, Wa

    def bijection(self, xws, yws, xys): # linear bijective alignment

        phrases = [[] for _ in xws]

        for xy in xys:
            score, (xr, yr) = xy
            phrases[xr[0]].append([score, xr, yr])

        phrases = [max(xys) for xys in phrases if xys]
        lens = [0, 0]

        for cand in phrases:

            score, xr, yr = cand

            if xr[0] < lens[0] or yr[0] < lens[1]: # phrase collision
                cand.append(False)
            else:
                cand.append(True)
                lens = [xr[1], yr[1]]

        phrases = [cand[:-1] for cand in phrases if cand[-1]]

        return phrases

    @staticmethod
    def _compare(x1, x2, y1, y2):

        if y2 <= x1 or x2 <= y1:
            return "DISJOINT"
        if y1 == x1 < x2 == y2:
            return "IDENTICAL"
        if y1 <= x1 < x2 <= y2:
            return "SUBSET"
        if x1 <= y1 < y2 <= x2:
            return "SUPERSET"

        return "OVERLAP"

    def extraction(self, xws, yws, xys): # non-linear alignment

        _xys = []

        for scores, (xr, yr), (xp, yp) in sorted(xys)[::-1]:

            updates = []
            removes = []

            for cand in _xys:

                _score, _xr, _yr, _state = cand

                if not _state:
                    continue

                v = {self._compare(*xr, *_xr), self._compare(*yr, *_yr)}

                if v == {"DISJOINT"}:
                    continue

                if v == {"SUBSET", "SUPERSET"}:
                    updates.append(cand)
                    continue

                if not v - {"IDENTICAL", "SUPERSET"}:
                    removes.append(cand)
                    continue

                # phrase collision
                # OVERLAP or ((DISJOINT or IDENTICAL) and SUBSET)
                break

            else: # if phrase collision not found

                for cand in updates:
                    _xr, _yr = cand[1:3]
                    xr = (min(xr[0], _xr[0]), max(xr[1], _xr[1]))
                    yr = (min(yr[0], _yr[0]), max(yr[1], _yr[1]))
                    cand[3] = False

                for cand in removes:
                    cand[3] = False

                _xys.append([scores[1], xr, yr, True])
                print(f"-> {scores[1]:.4f} {(xr, xp)} {(yr, yp)}")

        _xys = sorted(
            [cand[:-1] for cand in _xys if cand[-1]],
            key = lambda xy: xy[1]
        )

        return _xys

    def align(self, batch, method):

        for data in self.data_iter(batch):

            xws, yws, xys, Wa = self.score(*data)
            xys = getattr(self, method)(xws, yws, xys)
            phrase_scores = []
            sentence_score = 0

            _xws = [*xws]
            _yws = [*yws]
            phrase_scores = []
            sentence_score = 0

            for idx, (score, xr, yr) in enumerate(xys):

                tag = f"({idx}: "
                phrase_scores.append(score)
                sentence_score += (xr[1] - xr[0]) + (yr[1] - yr[0])

                for ws, (i, j) in zip((_xws, _yws), (xr, yr)):
                    ws[i] = tag + ws[i]
                    ws[j - 1] += " )"

            sentence_score /= len(xws) + len(yws)

            if self.verbose:
                print(f"src_aligned\t{" ".join(_xws)}")
                print(f"tgt_aligned\t{" ".join(_yws)}")
                print("phrase_scores", phrase_scores, sep = "\t")
                print("sentence_score", sentence_score, sep = "\t")
                heatmap(Wa, xws, yws)
                input()

            yield xws, yws, phrase_scores, sentence_score

if __name__ == "__main__":

    if len(sys.argv) not in (5, 6):
        sys.exit("Usage: %s src_lang tgt_lang sentence|bijection|extraction tokenized_bitext [-v]" % sys.argv[0])

    src_lang, tgt_lang, method, filename = sys.argv[1:5]

    aligner = phrase_aligner(
        src_lang = src_lang,
        tgt_lang = tgt_lang,
        batch_size = 1024,
        window_size = 3,
        thresholds = (0.01, 0.7),
        verbose = (len(sys.argv) == 6 and sys.argv[5] == "-v")
    )

    data_size = 0
    timer = time.time()

    for batch in batch_iter(filename, aligner.batch_size):

        data_size += len(batch)

        if method == "sentence":

            sentence_scores = aligner.sentence_similarity(batch)

            for line, sentence_similarity in zip(batch, sentence_scores):
                print(sentence_similarity, line, sep = "\t")

        if method in ("bijection", "extraction"):

            aligned = aligner.align(batch, method)

            for line, result in zip(batch, aligned):
                xws, yws, phrase_scores, sentence_score = result
                print(sentence_score, line, sep = "\t")

    print("%d lines (%.f seconds)" % (data_size, time.time() - timer), file = sys.stderr)
    timer = time.time()
