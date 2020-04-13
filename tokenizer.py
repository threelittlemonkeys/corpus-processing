import os
import sys
from collections import defaultdict

class tokenizer():

    def __init__(self, graph, lexicon):
        self.debug = True

        self.graph = dict()
        self.lexicon = dict()
        self.window_size = 0

        self.load_graph(graph)
        self.load_lexicon(lexicon)

    def load_graph(self, filename):
        fo = open(filename)
        for line in fo:
            line = line.strip()
            words = line.split(" ")
            for word in words:
                self.graph[word] = True
        fo.close()

    def load_lexicon(self, filename):
        fo = open(filename)
        for line in fo:
            word, tag, *_ = line.strip().split("\t")
            self.lexicon[word] = tag
            if len(word) > self.window_size:
                self.window_size = len(word)
        fo.close()

    def index(self, sent):
        idx = [x for x in enumerate(sent) if x[1] != " "]
        return idx

    def lexicalize(self, idx):
        table = [[] for _ in idx]
        for i in range(len(idx)):
            k = min(len(idx), i + self.window_size)
            for j in range(i + 1, k):
                w = "".join(c for _, c in idx[i:j])
                if w in self.graph:
                    table[i].append((w, None))
                if w in self.lexicon:
                    table[i].append((w, self.lexicon[w]))
        return table

    def analyze(self, sent):
        idx = self.index(sent)
        table = self.lexicalize(idx)
        print("sent =", sent)
        print("norm =", "".join(c for _, c in idx))
        for i, x in enumerate(table):
            print("table[%d] =" % i, x)
        input()

if __name__ == "__main__":
    tokenizer = tokenizer(
        lexicon = sys.path[0] + "/lexicon.csv",
        graph = sys.path[0] + "/graph.csv"
    )
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        tokenizer.analyze(line)
    fo.close()
