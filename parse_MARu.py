import sys
import re
import maru

# https://github.com/chomechome/maru

analyzer = maru.get_analyzer(tagger = "rnn", lemmatizer = "pymorphy")

for line in sys.stdin:

    tokens = line.strip().split(" ")
    analyzed = analyzer.analyze(tokens)

    words = []
    lemmas = []
    tags = []

    for morph in analyzed:

        word = morph.word
        lemma = morph.lemma
        tag = morph.tag

        words.append(word)
        lemmas.append(lemma)
        tags.append(tag)

    print("tokens =", tokens)
    print("lemmas =", lemmas)
    print("tags =", tags)
