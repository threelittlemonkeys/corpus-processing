import os
import sys
from utils import *

class nlu():

    def __init__(self, graph, lexicon):
        self.graph = dict()
        self.lexicon = dict()
        self.char_window_size = 0
        self.word_window_size = 0
        self.debug = True

        self.load_graph(graph)
        self.load_lexicon(lexicon)

        self.log("char_window_size = %d" % self.char_window_size)
        self.log()

    def log(self, *obj):
        if not self.debug:
            return
        print(*obj)

    def load_graph(self, filename):
        self.log("loading graph")
        fo = open(filename)
        for line in fo:
            line = line.strip()
            tokens = line.split(" ")
        fo.close()

    def load_lexicon(self, filename):
        self.log("loading lexicon")
        fo = open(filename)
        for line in fo:
            word, tag, *_ = line.strip().split("\t")
            if word not in self.lexicon:
                self.lexicon[word] = list()
            self.lexicon[word].append(tag)
            if len(word) > self.char_window_size:
                self.char_window_size = len(word)
        fo.close()

    def tokenize(self, sent):
        buf = ""
        sent += "\n"
        tokens = list()
        for c in sent:
            if c <= "\u0020":
                c = ""
            if c and not len(buf) \
            or isalpha_latin(c) and isalpha_latin(buf[-1]) \
            or isnumeric(c) and isnumeric(buf[-1]):
                buf += c
                continue
            if buf:
                w0 = "".join(buf) # surface form
                w1 = w0.lower() # normalized form
                end = 1 if c == "" else 0
                tokens.append((w0, w1, end))
            buf = c
        sent = "".join(nf + " " * end for sf, nf, end in tokens)
        return sent, tokens

    def lexicalize(self, tokens):
        table = [[] for _ in tokens]
        for i in range(len(tokens)):
            k = min(len(tokens), i + self.char_window_size)
            for j in range(i + 1, k + 1):
                word = [w1 for _, w1, _ in tokens[i:j]]
                if not isalpha_cjk(word):
                    continue
                word = "".join(word)
                if word in self.lexicon:
                    for tag in self.lexicon[word]:
                        table[i].append((word, j - i, tag))
            word = tokens[i][0]
            if isnumeric(word):
                table[i].append((word, 1, "NUM"))
            if not len(table[i]):
                table[i].append((word, 1, "UNK"))
        return table

    def generate_sequence():
        pass

    def analyze(self, sent):
        sent = sent.strip()
        self.log("sent =", sent)

        sent, tokens = self.tokenize(sent)
        self.log("norm =", sent)

        table = self.lexicalize(tokens)
        self.log("tokens =", tokens)

        for i, x in enumerate(table):
            self.log("table[%d] =" % i, x)

        input()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s text" % sys.argv[0])
    nlu = nlu(
        lexicon = "lexicon.csv",
        graph = "graph.csv"
    )
    fo = open(sys.argv[1])
    for line in fo:
        nlu.analyze(line)
    fo.close()
