import sys
import re

class xl_tokenizer():

    def __init__(self, src_lang, tgt_lang, phrase_maxlen):

        langs = (src_lang, tgt_lang)

        if "ja" in langs:
            # pip install mecab-python3 unidic-lite
            import MeCab
            self.ja_tagger = MeCab.Tagger()

        if "ko" in langs:
            # pip install python-mecab-ko
            import mecab
            self.ko_tagger = mecab.MeCab()

        alnum = "0-9A-Za-z\xC0-\xFF" # Latin-1
        alnum += "\u0100-\u017F" # Latin Extended-A
        alnum += "\u0180-\u024F" # Latin Extended-B
        alnum += "\u1E00-\u1EFF" # Latin Extended Additional
        alnum += "\uAC00-\uD7AF" # Hangul Syllables

        self.RE_NAN_L = re.compile("(?<=[^ %s])(?=[%s])" % (alnum, alnum))
        self.RE_NAN_R = re.compile("(?<=[%s])(?=[^ %s])" % (alnum, alnum))

        self.phrase_maxlen = phrase_maxlen

    def tokenize(self, line, lang):
        line = re.sub("\s+", " ", line)
        line = line.strip()
        line = line.lower()
        line = self.RE_NAN_L.sub(" ", line)
        line = self.RE_NAN_R.sub(" ", line)

        if lang == "en":
            return self.en(line)
        if lang == "ja":
            return self.ja(line)
        if lang == "ko":
            return self.ko(line)

        return line.split(" ")

    def en(self, x):
        x = re.sub("(?<=[a-z]{2})n ' t\\b", " not", x)
        x = re.sub("(?<=[a-z]) ' (?=(d|ll|m|s|re|ve)\\b)", " '", x)
        x = re.sub("\\bo ' clock\\b", "o'clock", x)
        return x.split(" ")

    def ja(self, x):
        morphs = list()
        result = [x.split("\t") for x in self.ja_tagger.parse(x).split("\n")]
        morphs = [(x[0], re.sub("-.*", "", x[4])) for x in result if len(x) == 8]
        morphs = [morph for morph, pos in morphs]
        return morphs

    def ko(self, x):
        morphs = list()
        result = self.ko_tagger.pos(x)
        for morph, pos in result:
            pos = pos.split("+")
            if not morphs:
                morphs.append([morph, pos])
                continue
            prev_morph, prev_pos = morphs[-1]
            if pos[0][0] in "EX" \
            or morph in "은는이가을를" and pos[0][0] == "J" \
            or prev_pos[0] == "NNB" and pos[0] == "VCP":
                morphs[-1][0] += morph
                morphs[-1][1] += pos
                continue
            morphs.append([morph, pos])
        morphs = [(morph, "+".join(pos)) for morph, pos in morphs]
        morphs = [morph for morph, pos in morphs]
        return morphs

    def phrase_iter(self, tokens):
        for i in range(len(tokens)):
            for j in range(i + 1, min(len(tokens), i + self.phrase_maxlen) + 1): 
                phrase = tokens[i:j]
                if self.validate_phrase(phrase):
                    yield (i, j), " ".join(phrase)

    def validate_phrase(self, phrase):
        if len(phrase) > 1 and phrase[-1] in (",", ".", "?", "!", "the"):
            return False
        return True

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: %s lang < text" % sys.argv[0])

    lang = sys.argv[1]

    tokenizer = xl_tokenizer(lang)

    for line in sys.stdin:
        line = line.strip()
        print(tokenizer.tokenize(line, lang))
