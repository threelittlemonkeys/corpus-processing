import sys
import re
import maru

# https://github.com/chomechome/maru

analyzer = maru.get_analyzer(tagger = "rnn", lemmatizer = "pymorphy")

for line in sys.stdin:

    tokens = line.strip().split(" ")
    analyzed = analyzer.analyze(tokens)

    words = list()
    lemmas = list()

    for morph in analyzed:

        word = morph.word
        lemma = morph.lemma
        tag = morph.tag

        words.append(word)
        lemmas.append(lemma)

    print(" ".join(tokens), end = "\t")
    print(" ".join(lemmas), end = "\n")
