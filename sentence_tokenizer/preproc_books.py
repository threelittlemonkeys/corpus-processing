import os
import sys
import re
from sentence_tokenizer import sentence_tokenizer

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

        if re.search("^[a-z]", line):
            continue

        if re.search("[^ A-Za-z0-9,.?!:;_$%&—()/'\"\n-]", line):
            continue

        line = re.sub("(?<=\.) (?=\.)", "", line)
        line = re.sub(" (?=[,.?!:;])", "", line)
        line = re.sub("(\.\"?)[0-9]+( |$)", "\\1\\2", line)

        sents = sentence_tokenizer.tokenize(line)
        wps = [sent.count(" ") + 1 for sent in sents] # words per sentence

        if len(sents) < 3:
            continue

        if sum(wps) / len(sents) < 12:
            continue

        if any("a" <= sent[0] <= "Z" for sent in sents):
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
