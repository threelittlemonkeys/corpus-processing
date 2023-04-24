import os
import sys
import re

class sentence_tokenizer():

    def __init__(self):

        self.dict = []

        path = (os.path.dirname(__file__) or ".") + "/"
        self.load_dict(path + "sentence_tokenizer.dict")

    def load_dict(self, filename):

        fo = open(filename)
        for line in fo:
            flag, pt = line.strip().split(" ", 1)
            self.dict.append((re.compile(pt), int(flag)))
        fo.close()

    def find_spans(self, line):

        spans = []

        for ro, flag in self.dict:
            for m in ro.finditer(line):
                spans.append((m.span(), flag))

        return sorted(spans, key = lambda x: x[0])

    def sbd(self, i, j, line, spans):

        if j == len(line) - 1:
            return True

        if not re.match("[.?!] ", line[j:j + 2]):
            return False

        if not line[i:j].count(" "):
            return False

        for span, v in spans:
            if span[0] <= j < span[1]:
                return v

        return True

    def tokenize(self, line):

        line = re.sub("\s+", " ", line).strip()
        line = re.sub("(?<=\.) (?=\.)", "", line)

        if not line:
            return []

        i = 0
        sents = []
        spans = self.find_spans(line)

        for j in range(len(line)):

            if not self.sbd(i, j, line, spans):
                continue

            sents.append(line[i:j + 1])
            i = j + 2

        return sents

if __name__ == "__main__":

    sentence_tokenizer = sentence_tokenizer()

    for line in sys.stdin:
        print(sentence_tokenizer.tokenize(line))
