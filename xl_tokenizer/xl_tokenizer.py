import sys
import re

class xl_tokenizer():

    _NUM = "0-9"
    _HIRAGANA = "\u3041-\u309F"
    _KATAKANA = "\u30A1-\u30FF"
    _HAN = "\u4E00-\u9FFF"
    _HANGEUL = "\uAC00-\uD7AF"

    _ALPHA = "A-Za-z"
    _ALPHA += "\xC0-\xFF" # Latin-1 Supplement
    _ALPHA += "\u0100-\u017F" # Latin Extended-A
    _ALPHA += "\u0180-\u024F" # Latin Extended-B
    _ALPHA += "\u1E00-\u1EFF" # Latin Extended Additional
    _ALPHA += _HIRAGANA + _KATAKANA + _HAN + _HANGEUL

    _ALNUM = _NUM + _ALPHA

    _RE_B = lambda x: re.compile("(?<=[%s])(?=[%s])" % (x, x))
    _RE_L = lambda x: re.compile("(?<=[^ %s])(?=[%s])" % (x, x))
    _RE_R = lambda x: re.compile("(?<=[%s])(?=[^ %s])" % (x, x))

    _ALPHA_L = _RE_L(_ALPHA)
    _ALPHA_R = _RE_R(_ALPHA)
    _NUM_L = _RE_L(_NUM)
    _NUM_R = _RE_R(_NUM)
    _NON_ALNUM = re.compile("[^%s]+" % _ALNUM)

    _KANJI_L = re.compile("(?<=[^ %sおご])(?=[%s])" % ((_HAN,) * 2))
    _KATAKANA_L = _RE_L(_KATAKANA)
    _KATAKANA_R = _RE_R(_KATAKANA)

    _HANGEUL_L = _RE_L(_HANGEUL)
    _HANGEUL_R = _RE_R(_HANGEUL)

    _HAN_B = _RE_B(_HAN)
    _HAN_L = _RE_L(_HAN)
    _HAN_R = _RE_R(_HAN)

    def __init__(self):

        self.taggers = {}

    def normalize(self, x, lc = True, alnum_only = False):

        if lc:
            x = x.lower()
        if alnum_only:
            x = RE_NON_ALNUM.sub(" ", x)
        x = re.sub("\s+", " ", x)
        x = x.strip()

        return x

    def import_tagger(self, lang):

        if lang == "ja":
            # pip install mecab-python3 unidic-lite
            import MeCab
            self.taggers[lang] = MeCab.Tagger()

        if lang == "ko":
            # pip install python-mecab-ko
            import mecab
            self.taggers[lang] = mecab.MeCab()

    def tokenize(self, lang, x, lc = True, alnum_only = False, use_tagger = False):

        x = self.normalize(x, lc, alnum_only)
        x = self._ALPHA_L.sub(" ", x)
        x = self._ALPHA_R.sub(" ", x)
        x = self._NUM_L.sub(" ", x)
        x = self._NUM_R.sub(" ", x)

        if use_tagger and lang not in self.taggers:
            use_tagger = False

        if lang == "en":
            return self.tokenize_en(x, use_tagger)
        if lang == "ja":
            return self.tokenize_ja(x, use_tagger)
        if lang == "ko":
            return self.tokenize_ko(x, use_tagger)
        if lang == "zh":
            return self.tokenize_zh(x, use_tagger)

        return x.split(" ")

    def tokenize_en(self, x, use_tagger):

        x = re.sub("(?<=[a-z]{2})n ' t\\b", "n't", x)
        x = re.sub("(?<=[a-z]) ' (?=(d|ll|m|s|re|ve)\\b)", " '", x)
        x = re.sub("\\bo ' clock\\b", "o'clock", x)

        return x.split(" ")

    def tokenize_ja(self, x, use_tagger):

        if not use_tagger:

            x = self._KANJI_L.sub(" ", x)
            x = self._KATAKANA_L.sub(" ", x)
            x = self._KATAKANA_R.sub(" ", x)

            return x.split(" ")

        out = [x.split("\t") for x in self.taggers["ja"].parse(x).split("\n")]
        out = [(x[0], re.sub("-.*", "", x[4])) for x in out if len(x) == 8]

        return [morph for morph, pos in out]

    def tokenize_ko(self, x, use_tagger):

        if not use_tagger:

            x = self._HANGEUL_L.sub(" ", x)
            x = self._HANGEUL_R.sub(" ", x)

            return x.split(" ")

        morphs = []

        for morph, pos in self.taggers["ko"].pos(x):
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

    def tokenize_zh(self, x, use_tagger):

        x = self._HAN_B.sub(" ", x)
        x = self._HAN_L.sub(" ", x)
        x = self._HAN_R.sub(" ", x)

        return x.split(" ")

if __name__ == "__main__":

    tokenizer = xl_tokenizer()

    line = "They've reviewed John's document."
    print(line)
    print(tokenizer.tokenize("en", line))
    print()

    line = "朝食は、朝起きて30分以内に取る。"
    tokenizer.import_tagger("ja")
    print(line)
    print(tokenizer.tokenize("ja", line))
    print(tokenizer.tokenize("ja", line, use_tagger = True))
    print()

    line = "아버지가007가방에들어가신다."
    tokenizer.import_tagger("ko")
    print(line)
    print(tokenizer.tokenize("ko", line))
    print(tokenizer.tokenize("ko", line, use_tagger = True))
