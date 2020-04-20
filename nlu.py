import os
import sys
from utils import *

class nlu():

    def __init__(self, graph_filename, lexicon_filename):
        self.lexicon = dict()
        self.graph = dict()
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
            _graph = list()
            line = line.strip()
            tag, *tokens = line.split(" ")
            print(line)
            for token in tokens:
                if token.isupper(): # tag
                    _graph.append((2, token))
                    continue
                # TODO surface form
                # TODO regular expression
                _graph.append((1, token)) # normalized form
            self.graph[_graph[0]] = (tag, _graph)
            print(self.graph)
        fo.close()

    def tokenize(self, sent):
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

    def detokenize(tokens):
        pass

    def lexicalize(self, tokens):
        table = [dict() for _ in tokens]
        for i in range(len(tokens)):
            k = min(len(tokens), i + self.char_window_size)
            for j in range(i + 1, k + 1):
                word = ("".join(nf for nf, *_ in tokens[i:j]),)
                if word in self.lexicon:
                    if word not in table[i]:
                        table[i][word] = set()
                    for feature in self.lexicon[word]:
                        table[i][word].add(feature)
            word = (tokens[i][0],)
            if word not in table[i]:
                table[i][word] = set()
            if isnumeric(word):
                table[i][word].add("NUM")
            if not len(table[i][word]):
                table[i][word].add("UNK")
        return table

    def generate_sequence():
        pass

    def analyze(self, sent):
        sent = sent.strip()
        self.log("sent =", sent)

        tokens = self.tokenize(sent)
        self.log("norm =", " ".join(nf for nf, *_, space in tokens))

        table = self.lexicalize(tokens)
        self.log("tokens =", tokens)

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
