import os
import sys
import re
from sentence_tokenizer import sentence_tokenizer

PRINT_FILTER = "out"
assert PRINT_FILTER in ("in", "out")

def validate(line):

    if re.search("^[a-z]", line):
        return None, False

    if re.search("[^ A-Za-z0-9,.?!:;_$%&—()/'\"\n-]", line):
        return None, False

    line = re.sub("(?<=\.) (?=\.)", "", line)
    line = re.sub(" (?=[,.?!:;])", "", line)
    line = re.sub("(\.\"?)[0-9]+( |$)", "\\1\\2", line)

    sents = sentence_tokenizer.tokenize(line)
    wps = [sent.count(" ") + 1 for sent in sents] # words per sentence

    if len(sents) < 3:
        return sents, False

    if sum(wps) / len(sents) < 12:
        return sents, False

    if any("a" <= sent[0] <= "Z" for sent in sents):
        return sents, False

    return sents, True

if __name__ == "__main__":

    pid = -1
    prev = -1
    paragraph = []

    sentence_tokenizer = sentence_tokenizer()

    for line in sys.stdin:

        line = re.sub("[\s_]+", " ", line).strip()

        if not line:
            continue

        pid += 1
        sents, flag = validate(line)

        if PRINT_FILTER == "out":
            if sents and not flag:
                print("\n".join(sents))
                print()
            continue

        if not flag:
            continue

        if pid != prev + 1 != 0:
            if len(paragraph) > 1 or len(paragraph[0]) >= 5:
                for _sents in paragraph:
                    for _sent in _sents:
                        print(_sent)
                    print()
                print()
            paragraph = []

        paragraph.append(sents)
        prev = pid

        '''
        print(f"paragraph[{pid}]")
        for _sent in sents:
            print(_sent)
        print()
        '''
