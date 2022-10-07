import sys
import re
from constants import *

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
