import sys
import re
import math
import time

class ibm_model1():

    def __init__(self, src_lang, tgt_lang):
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.data = []
        self.probs = [{}, {}]
        self.vocab = [{}, {}]
        self.dir = None # 0: forward, 1: backward
        self.num_epochs = 0

    @staticmethod
    def tokenize(lang, sent):

        alnum = "A-Za-z0-9"
        if lang == "ja":
            alnum += "\u30A1-\u30FA\u30FC"
        if lang == "ko":
            alnum += "\uAC00-\uD7AF"
        sent = re.sub(f"([^{alnum}])", " \\1 ", sent)

        sent = re.sub("\s{2,}", " ", sent)
        sent = sent.strip()
        sent = sent.split(" ")

        return sent

    @staticmethod
    def update_vocab(vocab, xs, ys):
        for x in ["", *xs]:
            if x not in vocab:
                vocab[x] = set()
            vocab[x].update(ys)

    def load_data(self, filename):
        fo = open(filename)
        for ln, line in enumerate(fo, 1):
            x, y = line.split("\t")
            xs = self.tokenize(self.src_lang, x)
            ys = self.tokenize(self.tgt_lang, y)
            self.data.append((xs, ys))
            self.update_vocab(self.vocab[0], xs, ys)
            self.update_vocab(self.vocab[1], ys, xs)
        fo.close()

    def data_iter(self):
        for xs, ys in self.data:
            if self.dir:
                xs, ys = ys, xs
            yield [""] + xs, ys

    def save_model(self, filename):

        fo = open(filename, "w")
        print("src_lang =", self.src_lang, file = fo)
        print("tgt_lang =", self.tgt_lang, file = fo)
        print("num_epochs =", self.num_epochs, file = fo)

        for d in range(2):
            cands = []
            for x in self.probs[d]:
                for y in self.probs[d][x]:
                    cands.append((self.probs[d][x][y], x, y))

            print(file = fo)
            for cand in sorted(cands, reverse = True):
                print(*cand, sep = "\t", file = fo)

        fo.close()

    def train(self, direction, num_epochs):

        self.dir = {"forward": 0, "backward": 1}[direction]
        src_vocab = self.vocab[self.dir]
        tgt_vocab = self.vocab[1 - self.dir]

        probs = {
            x: {y: 1 / len(tgt_vocab) for y in src_vocab[x]}
            for x in src_vocab
        }

        for epoch in range(1, num_epochs + 1):

            timer = time.time()
            counts = {x: {y: 0 for y in src_vocab[x]} for x in src_vocab}
            sum_counts = {x: 0 for x in src_vocab}

            for xs, ys in self.data_iter():
                for y in ys:
                    z = sum(probs[x][y] for x in xs)
                    for x in xs:
                        c = probs[x][y] / z
                        counts[x][y] += c
                        sum_counts[x] += c

            probs = {
                x: {y: counts[x][y] / sum_counts[x] for y in src_vocab[x]}
                for x in src_vocab
            }
            self.probs[self.dir] = probs
            self.num_epochs = epoch

            print("dir =", direction, end = ", ")
            print("epoch =", epoch, end = ", ")
            print("LL = %f" % self.log_likelihood(), end = ", ")
            print("PP = %f" % self.perplexity(), end = ", ")
            print("time = %fs" % (time.time() - timer))

    def topk(self, x, y, k):
        xs = [x] if x else self.vocab[1 - self.dir][y]
        ys = [y] if y else self.vocab[self.dir][x]
        ps = [((x, y), float("%f" % self.probs[self.dir][x][y])) for x in xs for y in ys]
        return sorted(ps, key = lambda x: -x[1])[:k]

    def sent_prob(self, xs, ys):
        '''
        e = 1
        p = math.prod(sum(self.probs[self.dir][x][y] for x in xs) for y in ys)
        p *= e / (len(xs) ** len(ys))
        '''
        p = math.prod(max(self.probs[self.dir][x][y] for x in xs) for y in ys)
        return p

    def log_likelihood(self):
        return sum(math.log(self.sent_prob(xs, ys)) for xs, ys in self.data_iter())

    def perplexity(self):
        p, z = 0, 0
        for xs, ys in self.data_iter():
            p += math.log(self.sent_prob(xs, ys), 2)
            z += len(ys)
        return 2 ** -(p / z)

if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.exit("Usage: %s L1 L2 corpus num_epochs" % sys.argv[0])

    model = ibm_model1(
        src_lang = sys.argv[1],
        tgt_lang = sys.argv[2]
    )

    filename = sys.argv[3]
    num_epochs = int(sys.argv[4])

    model.load_data(filename)
    model.train("forward", num_epochs)
    model.train("backward", num_epochs)
    model.save_model("%s.ibm_model1.epoch%d" % (filename, num_epochs))
