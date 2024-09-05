import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

def normalize(x, method = None):

    if method == "min-max":
        x -= x.min(axis = 1, keepdims = True)

    if method == "softmax":
        x = np.exp(x - x.max(axis = 1, keepdims = True))

    z = x.sum(axis = 1, keepdims = True)

    return np.divide(x, z, out = np.zeros_like(x), where = (z != 0))

def batch_iter(filename, batch_size):

    batch = []

    with open(filename) as fo:
        while True:
            line = fo.readline()
            if line:
                batch.append(line.strip())
                if len(batch) < batch_size:
                    continue
            if batch:
                yield batch
                batch.clear()
            if not line:
                break

def phrase_iter(tokens, phrase_maxlen):

    for i in range(len(tokens)):
        for j in range(i + 1, min(len(tokens), i + phrase_maxlen) + 1):
            phrase = tokens[i:j]
            if validate_phrase(phrase):
                yield (i, j), " ".join(phrase)

def validate_phrase(phrase):

    if len(phrase) > 1 and phrase[-1] in (",", ".", "?", "!", "the"):
        return False

    return True

def heatmap(xws, yws, xys):

    m = [[[] for _ in yws] for _ in xws]

    for score, (xr, yr), (xp, yp) in xys:
        for i in range(xr[0], xr[1]):
            for j in range(yr[0], yr[1]):
                m[i][j].append(score)

    m = np.array([[np.mean(y) for y in x] for x in m])
    m = normalize(m, method = "softmax")

    sns.heatmap(
        data = m,
        cmap = "Reds",
        cbar = False,
        xticklabels = yws,
        yticklabels = xws
    )

    plt.show()
