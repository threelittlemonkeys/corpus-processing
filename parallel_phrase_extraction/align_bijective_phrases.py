import sys
import re

flags = set(sys.argv[1:])

stats = {
    "ALIGNED": 0,
    "MISALIGNED" : 0,
    "MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT": 0,
    "MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC": 0
}

x2y = {}
y2x = {}
sents = {}

for ln, line in enumerate(sys.stdin):

    try:
        x, y = [re.sub("\s+", " ", e).strip() for e in line.split("\t")]
    except:
        sys.exit(f"Error: invalid line at line {ln}")

    xws = [w.strip() for w in re.split("[ ·・]", x)]
    yws = [w.strip() for w in re.split("[ ·・]", y)]

    if len(xws) == len(yws):
        cat = "ALIGNED"
        stats[cat] += 1
        if cat in flags:
            print(cat, (ln, x, y))

    if len(xws) != len(yws):
        cat = "MISALIGNED"
        stats[cat] += 1
        if cat in flags:
            print(cat, (ln, x, y))
        continue

    for xw, yw in zip(xws, yws):

        if xw not in x2y:
            x2y[xw] = {}
        if yw not in x2y[xw]:
            x2y[xw][yw] = 0
        x2y[xw][yw] += 1

        if yw not in y2x:
            y2x[yw] = {}
        if xw not in y2x[yw]:
            y2x[yw][xw] = 0
        y2x[yw][xw] += 1

        wp = (xw, yw)
        if wp not in sents:
            sents[wp] = set()
        sents[wp].add((ln, x, y))

cat = "MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT"
for xw, yws in x2y.items():
    if len(yws) > 1:
        if cat in flags:
            print(cat, xw)
            for yw, count in yws.items():
                print(cat, (yw, count, list(sents[(xw, yw)])[0]))
            print()
        stats[cat] += 1

cat = "MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC"
for yw, xws in y2x.items():
    if len(xws) > 1:
        if cat in flags:
            print(cat, yw)
            for xw, count in xws.items():
                print(cat, (xw, count, list(sents[(xw, yw)])[0]))
            print()
        stats[cat] += 1

print("NUM_LINES =", ln)
print("NUM_SRC_TOKENS =", len(x2y))
print("NUM_TGT_TOKENS =", len(y2x))

for cat, count in stats.items():
    print(cat, "=", count)
