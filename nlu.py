import os
import sys
from utils import *

class nlu():

    def __init__(self, graph_filename, lexicon_filename):
        self.graph = dict()
        self.lexicon = lexicon()
        self.char_window_size = 0
        self.word_window_size = 0
        self.debug = True

        self.load_graph(graph_filename)
        self.load_lexicon(lexicon_filename)

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

    def load_lexicon(self, filename):
        self.log("loading lexicon")
        fo = open(filename)
        for line in fo:
            entry, feature, *_ = line.strip().split("\t")
            entry = entry.split(" ")
            entry_len = sum(len(w) for w in entry)
            self.lexicon.add(entry, feature)
            if entry_len > self.char_window_size:
                self.char_window_size = entry_len
        fo.close()
        self.log("loaded %d lexicon entries" % self.lexicon.size)

    def tokenize(self, sent):
        buf = ""
        tokens = list()
        for i, c in enumerate(sent + "\n"):
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
                end = not c and i < len(sent) - 1
                tokens.append((w0, w1, end))
            buf = c
        sent = "".join(w1 + " " * end for _, w1, end in tokens)
        return sent, tokens

    def lexicalize(self, tokens):
        table = [dict() for _ in tokens]
        for i in range(len(tokens)):
            k = min(len(tokens), i + self.char_window_size)
            for j in range(i + 1, k + 1):
                word = ("".join(w1 for _, w1, _ in tokens[i:j]),)
                lexicon_node = self.lexicon.find(word)
                if lexicon_node:
                    if word not in table[i]:
                        table[i][word] = set()
                    for tag in lexicon_node.features:
                        table[i][word].add(tag)
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

        sent, tokens = self.tokenize(sent)
        self.log("sent =", sent)

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
