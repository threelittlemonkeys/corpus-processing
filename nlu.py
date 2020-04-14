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
            self.lexicon[word] = tag
            if len(word) > self.char_window_size:
                self.char_window_size = len(word)
        fo.close()

    def tokenize(self, sent):
        buf = ""
        words = list()
        for c in sent + "\n":
            if c <= "\u0020":
                c = ""
            if c and not len(buf) \
            or isalpha(c) and isalpha(buf[-1]) \
            or isnumeric(c) and isnumeric(buf[-1]):
                buf += c
                continue
            if buf:
                w0 = "".join(buf) # surface form
                w1 = w0.lower() # normalized form
                end = (c == "")
                words.append((w0, w1, end))
            buf = c
        sent = "".join(nf + " " * end for sf, nf, end in words)
        return sent, words

    def lexicalize(self, words):
        table = [[] for _ in words]
        for i in range(len(words)):
            k = min(len(words), i + self.char_window_size)
            for j in range(i + 1, k + 1):
                w = "".join(w1 for _, w1, _ in words[i:j])
                if w in self.graph:
                    table[i].append((w, None))
                if w in self.lexicon:
                    table[i].append((w, self.lexicon[w]))
            if not len(table[i]):
                w = words[i][0]
                if isnumeric(w):
                    table[i].append((w, "NUM"))
                else:
                    table[i].append((w, "UNK"))
        return table

    def generate_sequence():
        pass

    def analyze(self, sent):
        sent, words = self.tokenize(sent)
        table = self.lexicalize(words)
        self.log("sent =", sent)
        self.log("words =", [w1 for _, w1, _ in words])
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
