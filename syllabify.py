import sys
import re
import jamofy

_EN_C = "bdfhjklmnprstvwzðŋɡʃʒθ" # consonants
_EN_V = "aeiouæə" # vowels

_ENKO = {**{a: b for a, b in zip(
    "abdefhiklmnoprstuvzæðŋəɡθ",
    "ㅏㅂㄷㅔㅍㅎㅣㅋㄹㅁㄴㅗㅍㄹㅅㅌㅜㅂㅈㅐㄷㅇㅓㄱㅅ"
)}}

def syllabify(x):

    x = re.sub("[aàáɑάαὰ]", "a", x)
    x = re.sub("[eèéɛέ]", "e", x)
    x = re.sub("[oòóɔ]", "o", x)
    x = re.sub("[əʌΛ]", "ə", x)
    x = re.sub("[ìíɪ]", "i", x)
    x = re.sub("[uùúʊ]", "u", x)
    x = re.sub("[æǽӕ]", "æ", x)
    x = re.sub("ɝ", "ər", x)
    x = re.sub("ɫ", "l", x)
    x = re.sub("[rɹ]", "r", x)
    x = re.sub("ʤ", "dʒ", x)
    x = re.sub("ʧ", "tʃ", x)
    x = re.sub("[ˈˌ]", "", x)

    y, s = [], []

    for i, p in enumerate(x):

        j = i + 1
        # print(y, s, "<-", p)

        if p in _EN_C:

            if len(s) == 1 and p == "j":
                s[0] += p
                continue

            if len(s) in (1, 3) and s[-1] + p in ("dʒ", "tʃ"):
                s[-1] += p
                continue

            if len(s) == 2 and p == "r" and j < len(x) and x[j] in _EN_C:
                continue

            if len(s) in (1, 3) \
            or len(s) == 2 and (p not in "bklmnprŋ" or j < len(x) and x[j] in _EN_V + "jr"):
                y.append(s)
                s = []

            s.append(p)

        if p in _EN_V:

            if len(s) >= 2:
                y.append(s)
                s = []

            if len(s) == 0:
                s.append("")

            s.append(p)

    if s:
        y.append(s)

    return y

def combine_with_y(x):

    return {a:b for a, b in zip("aeouæə", "ㅑㅖㅛㅠㅒㅕ")}.get(x, x)

def combine_with_w(x):

    return {a:b for a, b in zip("aeioæə", "ㅘㅞㅣㅝㅙㅝ")}.get(x, x)

def ipa_to_hsyl(en) : # IPA to Hangeul syllables

    en = syllabify(en)
    print(en)

    for i, s in enumerate(en):

        j = i + 1

        if s[-1] == "r":
            s.pop()

        if len(s) == 1:

            if s[0][-1] in ("ʃ", "ʒ"):
                s.append("ㅣ")
            else:
                s.append("ㅡ")

        if len(s) >= 1:

            if s[0] == "":
                s[0] = "ㅇ"
            if s[0][-1:] == "j":
                s[0] = s[0][:-1]
                s[1] = combine_with_y(s[1])
            if s[0] == "w":
                s[0] = "ㅇ"
                s[1] = combine_with_w(s[1])
            if s[0] == "ʃ":
                s[0] = "ㅅ"
                s[1] = combine_with_y(s[1])
            if s[0] in ("ʒ", "dʒ"):
                s[0] = "ㅈ"
            if s[0] == "tʃ":
                s[0] = "ㅊ"

        s = [_ENKO.get(p, p) for p in s]

        if len(s) == 2:
            if j < len(en) and en[j][0] == "l":
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
