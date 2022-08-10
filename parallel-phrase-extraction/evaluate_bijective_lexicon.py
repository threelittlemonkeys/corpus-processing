import sys
import re

flags = set(sys.argv[1:])

stats = {
    "NUM_TOKENS_EQUAL": 0,
    "NUM_TOKENS_INEQUAL" : 0,
    "MULTIPLE_LEXICAL_TRANSLATIONS": 0
}

tokens = {}

for ln, line in enumerate(sys.stdin):
    x, y = [re.sub("\s+", " ", line).strip() for line in line.split("\t")]
    xws = [w.strip() for w in re.split("[ ・]", x)]
    yws = [w.strip() for w in re.split("[ ・]", y)]

    if len(xws) != len(yws):
        cat = "NUM_TOKENS_INEQUAL"
        stats[cat] += 1
        if cat in flags:
            print(cat, (x, y))
        continue

    if len(xws) == len(yws):
        cat = "NUM_TOKENS_EQUAL"
        stats[cat] += 1
        if cat in flags:
            print(cat, (x, y))

    for xw, yw in zip(xws, yws):
        if xw not in tokens:
            tokens[xw] = {}
        if yw not in tokens[xw]:
            tokens[xw][yw] = [0, set()]
        tokens[xw][yw][0] += 1
        tokens[xw][yw][1].add((x, y))

cat = "MULTIPLE_LEXICAL_TRANSLATIONS"
for xw, yws in tokens.items():
    if len(yws) > 1:
        if cat in flags:
            print(cat, xw)
            for yw, (count, lines) in yws.items():
                print(cat, (yw, count, list(lines)[0]))
        stats[cat] += 1

print("NUM_LINES =", ln)
print("NUM_TOKENS =", len(tokens))

for cat, count in stats.items():
    print(cat, "=", count)
