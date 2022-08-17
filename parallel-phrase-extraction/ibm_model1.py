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
        self.prob = [{}, {}]
        self.vocab = [{}, {}]
        self.min_prob = 1e-4

        self.dir = None # 0: forward, 1: backward
        self.epoch = None
        self.timer = None

    def load_vocab(self, filename):

        print("loading vocabulary")

        for i, lang in enumerate(("src", "tgt")):
            with open(filename + ".%s_vocab" % lang) as fo:
                self.itw[i] = fo.read().strip().split("\n")
                self.wti[i] = {w: i for i, w in enumerate(self.itw[i])}
                print("%s_vocab_size =" % lang, len(self.itw[i]))

    def data_iter(self, dir = None):

        if dir == None:
            dir = self.dir

        for xs, ys in self.data:
            if dir:
                xs, ys = ys, xs
            yield [0] + xs, ys

    def load_data(self, filename):

        print("loading data")

        fo = open(filename + ".csv")
        for line in fo:
            x, y = line.strip().split("\t")
            xs = list(map(int, x.split(" ")))
            ys = list(map(int, y.split(" ")))
            self.data.append((xs, ys))
        fo.close()

        for d in range(2):
            for xs, ys in self.data_iter(d):
                for x in xs:
                    if x not in self.vocab[d]:
                        self.vocab[d][x] = set()
                    self.vocab[d][x].update(ys)

    def load_model(self, filename):

        print("loading model")

        fo = open(filename)
        ln, line = 1, fo.readline()
        self.src_lang = re.search("^src_lang = (.+)\n", line).group(1)
        ln, line = 2, fo.readline()
        self.tgt_lang = re.search("^tgt_lang = (.+)\n", line).group(1)
        ln, line = 3, fo.readline()
        self.epoch = int(re.search("^epoch = (.+)\n", line).group(1))
        ln, line = 4, fo.readline()

        print("src_lang =", self.src_lang)
        print("tgt_lang =", self.tgt_lang)
        print("epoch =", self.epoch)

        for d in range(2):
            for ln, line in enumerate(fo, ln + 1):
                if line == "\n":
                    break
                p, x, y = re.search("^(.+)\t(.*)\t(.*)\n", line).groups()
                x = self.wti[d][x]
                y = self.wti[1 - d][y]
                if x not in self.prob[d]:
                    self.prob[d][x] = {}
                self.prob[d][x][y] = float(p)
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
            lines = []
            print(file = fo)
            for x in self.prob[d]:
                for y in self.prob[d][x]:
                    if self.prob[d][x][y] < self.min_prob:
                        continue
                    p = self.prob[d][x][y]
                    xw = self.itw[d][x]
                    yw = self.itw[1 - d][y]
                    lines.append((p, xw, yw))
            for line in sorted(lines, reverse = True):
                print(*line, sep = "\t", file = fo)

        print("saved model")
        fo.close()

    def _train(self, dir, num_epochs):

        print(f"training ibm_model1.prob.{dir}")

        self.dir = d = {"forward": 0, "backward": 1}[dir]
        src_vocab = self.vocab[d]
        tgt_vocab = self.vocab[1 - d]

        self.prob[d] = {
            x: {y: 1 / len(tgt_vocab) for y in src_vocab[x]}
            for x in src_vocab
        }

        for epoch in range(1, num_epochs + 1):

            self.timer = time.time()
            counts = {x: {y: 0 for y in src_vocab[x]} for x in src_vocab}
            sum_counts = {x: 0 for x in src_vocab}

            for xs, ys in self.data_iter():
                for y in ys:
                    z = sum(self.prob[d][x][y] for x in xs)
                    for x in xs:
                        c = self.prob[d][x][y] / z
                        counts[x][y] += c
                        sum_counts[x] += c

            self.prob[d] = {
                x: {y: counts[x][y] / sum_counts[x] for y in src_vocab[x]}
                for x in src_vocab
            }
            self.epoch = epoch

            self.evaluate()

    def train(self, num_epochs):
        model._train("forward", num_epochs)
        model._train("backward", num_epochs)

    def topk(self, x, y, k):
        xs = [x] if x else self.vocab[1][y]
        ys = [y] if y else self.vocab[0][x]
        ps = [((x, y), self.prob[0][x][y], self.prob[1][y][x]) for x in xs for y in ys]
        return sorted(ps, key = lambda x: -sum(x[1:]))[:k]

    def sent_prob(self, xs, ys):
        p = math.prod(
            sum(self.prob[self.dir].get(x, {}).get(y, self.min_prob) for x in xs)
            for y in ys
        )
        p *= 1 / (len(xs) ** len(ys))
        '''
        p = math.prod(
            max(self.prob[self.dir].get(x, {}).get(y, self.min_prob) for x in xs)
            for y in ys
        )
        '''
        return p if p else self.min_prob

    def evaluate(self):

        ll, pp, z = 0, 0, 0
        for xs, ys in self.data_iter():
            ll += math.log(self.sent_prob(xs, ys))
            pp += math.log(self.sent_prob(xs, ys), 2)
            z += len(ys)
        pp = 2 ** -(pp / z)

        print("epoch =", self.epoch, end = ", ")
        print("LL = %f" % ll, end = ", ")
        print("PP = %f" % pp, end = ", ")
        print("time = %fs" % (time.time() - self.timer))

if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.exit("Usage: %s src_lang tgt_lang data num_epochs" % sys.argv[0])

    model = ibm_model1(
        src_lang = sys.argv[1],
        tgt_lang = sys.argv[2]
    )

    filename = sys.argv[3]
    num_epochs = int(sys.argv[4])

    model.load_vocab(filename)
    model.load_data(filename)
    model.train(num_epochs)
    model.save_model("%s.ibm_model1.epoch%d" % (filename, num_epochs))
