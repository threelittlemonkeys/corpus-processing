import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from unicodedata import east_asian_width as eaw

# apt-get install fonts-nanum*
# fc-cache -fv
# python3 -c "import matplotlib; print(matplotlib.__path__)"
# cp /usr/share/fonts/truetype/nanum/Nanum* path/mpl-data/fonts/ttf/
# mpl.get_cachedir()
# rm fontlist.json

plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["font.size"] = 8
plt.rcParams["axes.unicode_minus"] = False

def cosine_similarity(x, y):

    return np.dot(x, y) / np.linalg.norm(x) * np.linalg.norm(y)

def normalize(x, axis, method):

    if method == "min-max":
        x -= x.min(axis = axis, keepdims = True)

    if method == "softmax":
        x = np.exp(x - x.max(axis = axis, keepdims = True))

    z = x.sum(axis = axis, keepdims = True)

    return np.divide(x, z, out = np.zeros_like(x), where = (z != 0))

class dataloader():

    def __init__(self, filename, batch_size):

        self.filename = filename
        self.data_size = 0
        self.batch_size = batch_size

    def batch(self):

        batch = []
        fo = open(self.filename)

        while True:
            line = fo.readline()
            if line:
                batch.append(line.strip())
                if len(batch) < self.batch_size:
                    continue
            if batch:
                self.data_size += len(batch)
                yield batch
                batch.clear()
            if not line:
                break

        fo.close()

def phrase_ngrams(tokens, phrase_maxlen):

    for i in range(len(tokens)):
        for j in range(i + 1, min(len(tokens), i + phrase_maxlen) + 1):
            phrase = tokens[i:j]
            if validate_phrase(phrase):
                yield (i, j), " ".join(phrase)

def validate_phrase(phrase):

    if len(phrase) == 1:
        return True

    if phrase[-1] in {",", ".", "?", "!", "the"}:
        return False

    return True

def bijection(xws, yws, xys): # linear bijective alignment

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

def extraction(xws, yws, xys): # non-linear alignment

    _xys = []

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

    for scores, (xr, yr), (xp, yp) in sorted(xys)[::-1]:

        updates = []
        removes = []

        for cand in _xys:

            _score, _xr, _yr, _state = cand

            if not _state:
                continue

            v = {_compare(*xr, *_xr), _compare(*yr, *_yr)}

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

    _xys = sorted(
        [cand[:-1] for cand in _xys if cand[-1]],
        key = lambda xy: xy[1]
    )

    return _xys

def heatmap(*ms):

    _, axs = plt.subplots(ncols = len(ms))

    for ax, (m, xws, yws) in zip(axs, ms):
        sns.heatmap(
            data = m,
            cmap = "Reds",
            cbar = False,
            ax = ax,
            xticklabels = yws,
            yticklabels = xws,
            annot = False
        )

    plt.show()

def text_heatmap(m, xws, yws, threshold):

    xi = [str(i)[-1] for i in range(len(xws))]
    yi = [str(i)[-1] for i in range(len(yws))]

    hl = "+" + "-" * (len(xws) * 2 + 9) + "+" # horizontal line
    nd = " " * 7 # indent

    xws = [[c + ("" if eaw(c) == "W" else " ") for c in f"{w:<5.5}"] for w in xws]
    yws = [f"{w:>5.5}" for w in yws]

    print(hl)
    print("\n".join(" ".join(
        ["|", w, i, *[" " if y < threshold else "*" for y in ys], "|"]
        ) for (ys, i, w) in zip(m, yi, yws)
    ))
    print(" ".join(["|", nd, *xi, "|"]))
    print("\n".join(" ".join(["|", nd[:-1], "".join(cs), "|"]) for cs in zip(*xws)))
    print(hl)
