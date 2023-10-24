import sys
import re
import jamofy

_EN_C = "bdfhkmnpstvzðŋɡɫɹʃʒθ" # consonants
_EN_V = "aeijouwæɑɔəɛɝɪʊ" # vowels and semivowels

_ENKO = {
    **{a: b for a, b in zip(
        "aebdfhikmnopstuvwzæðŋɑɔəɛɝɡɪɫɹʊθ",
        "ㅏㅔㅂㄷㅍㅎㅣㅋㅁㄴㅗㅍㅅㅌㅜㅂㅜㅈㅐㄷㅇㅏㅗㅓㅔㅓㄱㅣㄹㄹㅜㅅ"
    )},
    **{"j" + a: b for a, b in zip(
        "aeiouæɑɔəɛɝɪʊ",
        "ㅑㅖㅣㅛㅠㅒㅑㅛㅕㅖㅕㅣㅠ",
    )},
    **{"w" + a: b for a, b in zip(
        "aeiouæɑɔəɛɝɪʊ",
        "ㅘㅞㅟㅝㅜㅙㅘㅝㅝㅞㅝㅟㅜ",
    )}
}

def syllabify(x):

    x = re.sub("ɝ", "əɹ", x)
    y, s = [], []

    for i, p in enumerate(x):

        j = i + 1
        # print(y, s, "<-", p)

        if s and p in "ˈˌ":
            y.append(s)
            s = []

        if p in _EN_C:

            if len(s) in (1, 3) and s[-1] + p in ("dʒ", "tʃ"):
                s[-1] += p
                continue

            if len(s) == 2 and p == "ɹ" and j < len(x) and x[j] in _EN_C:
                continue

            if len(s) in (1, 3) \
            or len(s) == 2 and (p not in "bmnkpŋɫɹ" or j < len(x) and x[j] in _EN_V):
                y.append(s)
                s = []

            s.append(p)

        if p in _EN_V:

            if len(s) == 2 and s[1] in "jw":
                s[1] += p
                continue

            if len(s) >= 2:
                y.append(s)
                s = []

            if len(s) == 0:
                s.append("")

            s.append(p)

    if s:
        y.append(s)

    return y

def palatalize(x):

    return {a:b for a, b in zip("ㅏㅐㅓㅔㅗㅜ", "ㅑㅒㅕㅖㅛㅠ")}.get(x, x)

def ipa_to_hsyl(en) : # IPA to Hangeul syllables

    en = syllabify(en)
    print(en)

    for i, s in enumerate(en):

        j = i + 1

        if s[-1] == "ɹ":
            s.pop()

        s = [_ENKO.get(p, p) for p in s]

        if len(s) == 1:
            if s[0][-1] in ("ʃ", "ʒ"):
                s.append("ㅣ")
            else:
                s.append("ㅡ")

        if len(s) >= 1:
            if s[0] == "ʃ":
                s[1] = palatalize(s[1])
            s[0] = {"": "ㅇ", "ʃ": "ㅅ", "ʒ": "ㅈ", "dʒ": "ㅈ", "tʃ": "ㅊ"}.get(s[0], s[0])

        if len(s) == 2:
            if j < len(en) and en[j][0] == "ɫ":
                s.append("ㄹ")

        if len(s) == 3:
            if s[2] == "ㅋ":
                s[2] = "ㄱ"
            if s[2] == "ㅍ":
                s[2] = "ㅂ"

        en[i] = "".join(s)

    ko = "".join(jamofy.jamo_to_hsyl(s) for s in en)

    return ko

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: %s enko < filename")

    method = sys.argv[1]

    for line in sys.stdin:

        line = line.strip()
        a, b = line.split("\t")

        if method == "enko":
            print(a, b, ipa_to_hsyl(b), sep = "\t")
