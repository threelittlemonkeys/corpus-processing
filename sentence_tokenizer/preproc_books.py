import os
import sys
import re
from sentence_tokenizer import sentence_tokenizer

FILTER = sys.argv[1]
assert FILTER in ("in", "out")

def validate(line):

    line = re.sub("(?<=\.) (?=\.)", "", line)
    line = re.sub("(?<=\() ", "", line)
    line = re.sub(" (?=[,.?!:;)])", "", line)
    line = re.sub("(\.\"?)[0-9]+( |$)", "\\1\\2", line)

    sents = sentence_tokenizer.tokenize(line)
    wps = [sent.count(" ") + 1 for sent in sents] # words per sentence

    if re.search("^[a-z]", line):
        return sents, False

    if re.search("[^ A-Za-z0-9,.?!:;#$%&£—()/'\"\n-]", line):
        return sents, False

    if sum(wps) / len(wps) < 8:
        return sents, False

    if any("a" <= sent[0] <= "z" for sent in sents):
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
        out, flag = validate(line)

        if not flag:
            if out and FILTER == "out":
                print("\n".join(out))
                print()
            continue

        if pid > prev + 1 != 0:

            spp = [len(sents) for sents in paragraph] # sentences per paragraph
            flag = False

            if len(spp) > 1 and sum(spp) / len(spp) > 2 or spp[0] >= 10:
                if FILTER == "in":
                    flag = True
            elif FILTER == "out":
                flag = True

            if flag:
                for sents in paragraph:
                    for sent in sents:
                        print(sent)
                    print()
                print()

            paragraph = []

        paragraph.append(out)
        prev = pid

        '''
        print(f"paragraph[{pid}]")
        for sent in sents:
            print(sent)
        print()
        '''
