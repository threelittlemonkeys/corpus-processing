import sys
import re

CONV = dict()
with open("char_table.tsv") as fo:
    for line in fo:
        a, b = line.strip().split("\t")
        CONV[a] = b
CONV_MAXLEN = len(max(CONV.keys(), key = len))

def clean_text(line, verbose = False):

    raw = line.strip()

    # control characters
    line = re.sub("[\u0000-\u001F\u007F\u0080-\u009F]+", " ", line)

    # whitespace characters
    line = re.sub("[\u0020\u00A0\u2000-\u200B\u202F\u205F\u3000]+", " ", line)

    # private use area
    line = re.sub("[\uE000-\uF8FF]", " ", line)

    # byte order marks
    line = re.sub("[\uFEFF\uFFFE]", " ", line)

    # full width characters
    line = "".join(chr(ord(c) - 0xFEE0) if "\uFF01" <= c <= "\uFF5E" else c for c in line)

    # convert CJK characters
    i = 0
    while i < len(line):
        for j in range(min(len(line), i + CONV_MAXLEN), 0, -1):
            w = line[i:j]
            if w in CONV:
                line = line[:i] + CONV[w] + line[j:]
                i += len(CONV[w])
                break
        else:
            i += 1

    line = re.sub(" {2,}", " ", line)
    line = line.strip()

    return line

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: %s filename [-v]" % sys.argv[0])

    verbose = (len(sys.argv) == 3 and sys.argv[2] == "-v")

    fo = open(sys.argv[1])
    for raw in fo:
        line = clean_text(raw, verbose)
        if not verbose:
            print(line)
        elif raw != line:
            print("<", raw, end = "")
            print(">", line, "\n")
    fo.close()
