import os
import sys
import re
import html
import time

path = (os.path.dirname(__file__) or ".") + "/"
CONV = dict()
with open(path + "char_table.tsv") as fo:
    for line in fo:
        a, b = line.strip().split("\t")
        CONV[a] = b
CONV_MAXLEN = len(max(CONV.keys(), key = len))

def clean_text(line, verbose = False):

    # full width characters
    line = "".join(chr(ord(c) - 0xFEE0) if "\uFF01" <= c <= "\uFF5E" else c for c in line)

    # mixed width CJK characters
    i = 0
    while i < len(line):
        for j in range(min(len(line), i + CONV_MAXLEN), i, -1):
            w = line[i:j]
            if w in CONV:
                line = line[:i] + CONV[w] + line[j:]
                i += len(CONV[w])
                break
        else:
            i += 1

    # HTML entities
    line = html.unescape(line)

    # control characters
    line = re.sub("[\x00-\x1F\x7F\x80-\x9F]+", " ", line)

    # whitespace characters
    line = re.sub("[\x20\xA0\u2000-\u200B\u202F\u205F\u3000]+", " ", line)

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

    verbose = (len(sys.argv) == 3 and sys.argv[2] == "-v")

    timer = time.time()
    fo = open(sys.argv[1])
    for ln, raw in enumerate(fo, 1):
        line = clean_text(raw, verbose)
        if not verbose:
            print(line)
        elif raw != line:
            print("<", raw, end = "")
            print(">", line, "\n")
        if ln % 100000 == 0:
            print("%d sentence pairs" % ln, file = sys.stderr)

    fo.close()

    print("%f seconds" % (time.time() - timer), file = sys.stderr)
