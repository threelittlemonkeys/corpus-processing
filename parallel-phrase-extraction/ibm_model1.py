import sys
import re
import math
import time

class ibm_model1():

    def __init__(self, src_lang = None, tgt_lang = None):
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.data = []
        self.itw = [[], []]
        self.wti = [{}, {}]
        self.probs = [{}, {}]
        self.vocab = [{}, {}]
        self.dir = None # 0: forward, 1: backward
        self.epoch = None

    def load_vocab(self, filename):
        for i, lang in enumerate(("src", "tgt")):
            with open(filename + ".%s_vocab" % lang) as fo:
                self.itw[i] = fo.read().strip().split("\n")
                self.wti[i] = {w: i for i, w in enumerate(self.itw[i])}
                print("%s_vocab_size =" % lang, len(self.itw[i]))

    def load_data(self, filename):

        print("loading data")
        self.load_vocab(filename)

        fo = open(filename + ".csv")
        for line in fo:
            x, y = line.strip().split("\t")
            xs = list(map(int, x.split(" ")))
            ys = list(map(int, y.split(" ")))
            self.data.append((xs, ys))
            for d in range(2):
                if d:
                    xs, ys = ys, xs
                for x in [0] + xs:
                    if x not in self.vocab[d]:
                        self.vocab[d][x] = set()
                    self.vocab[d][x].update(ys)
        fo.close()

    def data_iter(self):
        for xs, ys in self.data:
            if self.dir:
                xs, ys = ys, xs
            yield [0] + xs, ys

    def load_model(self, filename):

        print("loading model")
        self.load_vocab(re.sub("\.ibm_model1\.epoch[0-9]+$", "", filename))

        fo = open(filename)
        ln, line = 1, fo.readline()
        self.src_lang = re.search("^src_lang = (.+)\n", line).group(1)
        ln, line = 2, fo.readline()
        self.tgt_lang = re.search("^tgt_lang = (.+)\n", line).group(1)
        ln, line = 3, fo.readline()
        self.epoch = int(re.search("^epoch = (.+)\n", line).group(1))
        ln, line = 4, fo.readline()
        for d in range(2):
            for ln, line in enumerate(fo, ln + 1):
                if line == "\n":
                    break
                prob, x, y = re.search("^(.+)\t(.*)\t(.*)\n", line).groups()
                x = self.wti[d][x]
                y = self.wti[1 - d][y]
                if x not in self.probs[d]:
                    self.probs[d][x] = {}
                self.probs[d][x][y] = float(prob)
                if x not in self.vocab[d]:
                    self.vocab[d][x] = set()
                self.vocab[d][x].add(y)
        fo.close()

    def save_model(self, filename):

        fo = open(filename, "w")
        print("src_lang =", self.src_lang, file = fo)
        print("tgt_lang =", self.tgt_lang, file = fo)
        print("epoch =", self.epoch, file = fo)

        for d in range(2):
            cands = []
            for x in self.probs[d]:
                for y in self.probs[d][x]:
                    cands.append((self.probs[d][x][y], self.itw[d][x], self.itw[1 - d][y]))

            print(file = fo)
            for cand in sorted(cands, reverse = True):
                print(*cand, sep = "\t", file = fo)

        print("saved model")
        fo.close()

    def _train(self, direction, num_epochs):

        print(f"training ibm_model1.probs.{direction}")

        self.dir = {"forward": 0, "backward": 1}[direction]
        src_vocab = self.vocab[self.dir]
        tgt_vocab = self.vocab[1 - self.dir]

        self.probs[self.dir] = {
            x: {y: 1 / len(tgt_vocab) for y in src_vocab[x]}
            for x in src_vocab
        }

        for epoch in range(1, num_epochs + 1):

            timer = time.time()
            counts = {x: {y: 0 for y in src_vocab[x]} for x in src_vocab}
            sum_counts = {x: 0 for x in src_vocab}

            for xs, ys in self.data_iter():
                for y in ys:
                    z = sum(self.probs[self.dir][x][y] for x in xs)
                    for x in xs:
                        c = self.probs[self.dir][x][y] / z
                        counts[x][y] += c
                        sum_counts[x] += c

            self.probs[self.dir] = {
                x: {y: counts[x][y] / sum_counts[x] for y in src_vocab[x]}
                for x in src_vocab
            }
            self.epoch = epoch

            print("epoch =", epoch, end = ", ")
            print("LL = %f" % self.log_likelihood(), end = ", ")
            print("PP = %f" % self.perplexity(), end = ", ")
            print("time = %fs" % (time.time() - timer))

    def train(self, num_epochs):
        model._train("forward", num_epochs)
        model._train("backward", num_epochs)

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
        sys.exit("Usage: %s src_lang tgt_lang data num_epochs" % sys.argv[0])

    model = ibm_model1(
        src_lang = sys.argv[1],
        tgt_lang = sys.argv[2]
    )

    filename = sys.argv[3]
    num_epochs = int(sys.argv[4])

    model.load_data(filename)
    model.train(num_epochs)
    model.save_model("%s.ibm_model1.epoch%d" % (filename, num_epochs))
