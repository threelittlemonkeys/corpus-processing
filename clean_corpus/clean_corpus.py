import os
import sys
import re
import html

class corpus_cleaner():

    def __init__(self):
        self.path = (os.path.dirname(__file__) or ".") + "/"
        self.table, self.maxlen = self.load_table("char_table.tsv")

    def load_table(self, filename):
        table = dict()
        with open(self.path + filename) as fo:
            for line in fo:
                a, b = line.strip().split("\t")
                table[a] = b
        maxlen = len(max(table.keys(), key = len))
        return table, maxlen

    def clean(self, line):

        # full width characters
        line = "".join(chr(ord(c) - 0xFEE0) if "\uFF01" <= c <= "\uFF5E" else c for c in line)

        # mixed width CJK characters
        i = 0
        while i < len(line):
            for j in range(min(len(line), i + self.maxlen), i, -1):
                w = line[i:j]
                if w in self.table:
                    line = line[:i] + self.table[w] + line[j:]
                    i += len(self.table[w])
                    break
            else:
                i += 1

        # HTML entities
        line = html.unescape(line)

        # control characters
        line = re.sub("[\x00-\x1F\x7F\x80-\x9F]+", " ", line)

        # whitespace characters
        line = re.sub("[\x20\xA0\u2000-\u200F\u202F\u205F\u3000]+", " ", line)

        # private use area
        line = re.sub("[\uE000-\uF8FF]", " ", line)

        # byte order marks
        line = re.sub("[\uFEFF\uFFFE]", " ", line)

        # punctuation marks
        line = re.sub(r"(?<=\S)’(?=(d|ll|m|re|s|t|ve)\b)", "'", line, flags = re.I)

        line = re.sub(" {2,}", " ", line)
        line = line.strip()

        return line

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: %s filename [-v]" % sys.argv[0])

    cleaner = corpus_cleaner()
    verbose = (len(sys.argv) == 3 and sys.argv[2] == "-v")

    fo = open(sys.argv[1])
    for ln, raw in enumerate(fo, 1):
        line = cleaner.clean(raw)
        if not verbose:
            print(line)
        elif raw != line:
            print("<", raw, end = "")
            print(">", line, "\n")
        if ln % 100000 == 0:
            print("%d sentence pairs" % ln, file = sys.stderr)

    fo.close()
