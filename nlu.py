import os
import sys
from utils import *

class nlu():

    def __init__(self, graph_filename, lexicon_filename):
        self.lexicon = dict()
        self.graph = tree()
        self.char_window_size = 0
        self.word_window_size = 0
        self.debug = True

        self.load_lexicon(lexicon_filename)
        self.load_graph(graph_filename)

        self.log("char_window_size = %d" % self.char_window_size)
        self.log()

    def log(self, *args):
        if not self.debug:
            return
        print(*args)

    def load_lexicon(self, filename):
        self.log("loading lexicon")
        fo = open(filename)
        for line in fo:
            entry, feature, *_ = line.strip().split("\t")
            entry = tuple(entry.split(" "))
            entry_len = sum(len(w) for w in entry)
            if entry not in self.lexicon:
                self.lexicon[entry] = list()
            self.lexicon[entry].append(feature)
            if entry_len > self.char_window_size:
                self.char_window_size = entry_len
        fo.close()
        self.log("loaded %d lexicon entries" % len(self.lexicon))

    def load_graph(self, filename):
        self.log("loading graph")
        fo = open(filename)
        for line in fo:
            _tokens = list()
            feature, *tokens = line.strip().split(" ")
            for token in tokens:
                if token.isupper(): # feature
                    _tokens.append((2, token))
                    continue
                # TODO surface form
                # TODO regular expression
                _tokens.append((1, token)) # normalized form
            self.graph.add(tokens, feature)
        print(self.graph.node)
        print(sizeof(self.graph))
        fo.close()

    @staticmethod
    def tokenize(sent):
        sf = "" # surface form
        bound = False
        tokens = list()
        for i, c in enumerate(sent + "\n"):
            if c <= "\u0020":
                c = ""
            elif not len(sf) \
            or isalpha_latin(c) and isalpha_latin(sf[-1]) \
            or isnumeric(c) and isnumeric(sf[-1]):
                sf += c
                continue
            if sf:
                nf = sf.lower() # normalized form
                bound = len(sf) == 1 and isalpha_cjk(sf)
                space = not c and i < len(sent) - 1 # trailing space
                tokens.append((nf, sf, bound, space))
            sf = c
        return tokens

    @staticmethod
    def detokenize(tokens):
        _bound = False
        phr_sf = list()
        phr_nf = list()
        for nf, sf, bound, _ in tokens:
            if not (bound and _bound):
                phr_sf.append("")
                phr_nf.append("")
            phr_sf[-1] += nf
            phr_nf[-1] += nf
            _bound = bound
        return (tuple(phr_sf), tuple(phr_nf), len(tokens))

    def lexicalize(self, tokens):
        table = list(dict() for _ in tokens)
        for i in range(len(tokens)):
            k = min(len(tokens), i + self.char_window_size)
            for j in range(i + 1, k + 1):
                _, phr_nf, phr_len = self.detokenize(tokens[i:j])
                if phr_nf in self.lexicon:
                    phr = (phr_nf, phr_len)
                    if phr not in table[i]:
                        table[i][phr] = set()
                    for feature in self.lexicon[phr[0]]:
                        table[i][phr].add(feature)
            word = ((tokens[i][0],), 1)
            if word not in table[i]:
                table[i][word] = set()
            if isnumeric(word[0]):
                table[i][word].add("NUM")
            if not len(table[i][word]):
                table[i][word].add("UNK")
        return table

    def analyze(self, sent):
        sent = sent.strip()
        self.log("sent =", sent)

        tokens = self.tokenize(sent)
        self.log("tokens =", [nf for nf, *_, space in tokens])

        table = self.lexicalize(tokens)

        for i, x in enumerate(table):
            self.log("table[%d] =" % i, x)

        input()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s text" % sys.argv[0])
    nlu = nlu(
        lexicon_filename = "lexicon.csv",
        graph_filename = "graph.csv"
    )
    fo = open(sys.argv[1])
    for line in fo:
        nlu.analyze(line)
    fo.close()
