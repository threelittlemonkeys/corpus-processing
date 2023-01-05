import sys
import re

EN = "A-Za-z"
JA_HIRAGANA = "\u3041-\u3096\u3099-\u309C"
JA_KATAKANA = "\u30A1-\u30FA\u30FC"
JA_KANJI = "\u4E00-\u9FFF"
JA = JA_HIRAGANA + JA_KATAKANA + JA_KANJI
KO = "\uAC00-\uD7AF"
ZH = "\u4E00-\u9FFF"

NUM = "0-9"

ALPHA = EN
ALPHA += "\xC0-\xFF" # Latin-1 Supplement
ALPHA += "\u0100-\u017F" # Latin Extended-A
ALPHA += "\u0180-\u024F" # Latin Extended-B
ALPHA += "\u1E00-\u1EFF" # Latin Extended Additional
ALPHA += JA + KO + ZH
ALNUM = ALPHA + NUM

RE_B = lambda x: re.compile("(?<=[%s])(?=[%s])" % (x, x))
RE_L = lambda x: re.compile("(?<=[^ %s])(?=[%s])" % (x, x))
RE_R = lambda x: re.compile("(?<=[%s])(?=[^ %s])" % (x, x))

RE_ALPHA_L = RE_L(ALPHA)
RE_ALPHA_R = RE_R(ALPHA)
RE_NUM_L = RE_L(NUM)
RE_NUM_R = RE_R(NUM)
RE_NON_ALNUM = re.compile("[^%s]+" % ALNUM)

RE_EN_L = RE_L(EN)
RE_EN_R = RE_R(EN)

RE_JA_KANJI_L = re.compile("(?<=[^ %sおご])(?=[%s])" % ((JA_KANJI,) * 2))
RE_JA_KATAKANA_L = RE_L(JA_KATAKANA)
RE_JA_KATAKANA_R = RE_R(JA_KATAKANA)

RE_KO_L = RE_L(KO)
RE_KO_R = RE_R(KO)

RE_ZH_B = RE_B(ZH)
RE_ZH_L = RE_L(ZH)
RE_ZH_R = RE_R(ZH)

taggers = {}

def import_tagger(lang):

    taggers[lang] = None

    if lang == "ja":
        # pip install mecab-python3 unidic-lite
        import MeCab
        taggers[lang] = MeCab.Tagger()

    if lang == "ko":
        # pip install python-mecab-ko
        import mecab
        taggers[lang] = mecab.MeCab()

def normalize(txt, lc = True, alnum_only = False):

    if lc: txt = txt.lower()

    if alnum_only:
       txt = RE_NON_ALNUM.sub(" ", txt)

    txt = re.sub("\s+", " ", txt)
    txt = txt.strip()

    return txt

def tokenize(lang, txt, lc = True, alnum_only = False, use_tagger = False):

    txt = normalize(txt, lc, alnum_only)

    txt = RE_ALPHA_L.sub(" ", txt)
    txt = RE_ALPHA_R.sub(" ", txt)
    txt = RE_NUM_L.sub(" ", txt)
    txt = RE_NUM_R.sub(" ", txt)

    if use_tagger and lang not in taggers:
        import_tagger(lang)
    tagger = taggers[lang] if use_tagger else None

    if lang == "en":
        txt = tokenize_en(txt, tagger)
    if lang == "ja":
        txt = tokenize_ja(txt, tagger)
    if lang == "ko":
        txt = tokenize_ko(txt, tagger)
    if lang == "zh":
        txt = tokenize_zh(txt, tagger)

    return txt

def tokenize_en(txt, tagger):

    if not tagger:
        return txt.split(" ")

    txt = re.sub("(?<=[a-z]{2})n ' t\\b", "n't", txt)
    txt = re.sub("(?<=[a-z]) ' (?=(d|ll|m|s|re|ve)\\b)", " '", txt)
    txt = re.sub("\\bo ' clock\\b", "o'clock", txt)

    return txt.split(" ")

def tokenize_ja(x, tagger):

    if not tagger:

        x = RE_EN_L.sub(" ", x)
        x = RE_EN_R.sub(" ", x)
        x = RE_JA_KANJI_L.sub(" ", x)
        x = RE_JA_KATAKANA_L.sub(" ", x)
        x = RE_JA_KATAKANA_R.sub(" ", x)

        return x.split(" ")

    morphs = []
    result = [x.split("\t") for x in tagger.parse(x).split("\n")]
    morphs = [(x[0], re.sub("-.*", "", x[4])) for x in result if len(x) == 8]
    morphs = [morph for morph, pos in morphs]

    return morphs

def tokenize_ko(x, tagger):

    if not tagger:

        x = RE_KO_L.sub(" ", x)
        x = RE_KO_R.sub(" ", x)

        return x.split(" ")

    morphs = []
    result = tagger.pos(x)

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

def tokenize_zh(x, tagger):

    if not tagger:
        pass

    x = RE_ZH_B.sub(" ", x)
    x = RE_ZH_L.sub(" ", x)
    x = RE_ZH_R.sub(" ", x)

    return x.split(" ")

if __name__ == "__main__":
    pass
