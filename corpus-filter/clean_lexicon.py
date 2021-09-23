import sys

lexicon = dict()

for line in sys.stdin:
    line = line.strip()
    a, *bs = line.split("\t")
    if a not in lexicon:
        lexicon[a] = set()
    for b in bs:
        lexicon[a].add(b)

for a, bs in sorted(lexicon.items()):
    print(a, *sorted(bs), sep = "\t")
