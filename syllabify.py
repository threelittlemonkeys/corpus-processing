import sys
import re
import jamofy

# sonority hierarchy
# vowels > glides > liquids > nasals > fricatives > affricates > plosives

_EN_C = "bdfghjklmnprstvwzðŋɡʃʒθ" # consonants
_EN_V = "aeiouæə" # vowels

_ENKO = {**{a: b for a, b in zip(
    "bdfghjklmnprstvwzðŋɡʃʒθ",
    "ㅏㅂㄷㅔㅍㄱㅎㅣㅋㄹㅁㄴㅗㅍㄹㅅㅌㅜㅂㅈㅐㄷㅇㅓㄱㅅ"
)}}

def normalize(x):

    x = re.sub("\s+", " ", x).strip()

    x = re.sub("[aàáɑɒάαὰ]", "a", x)
    x = re.sub("[eèéɛέὲ]", "e", x)
    x = re.sub("[iìíɪ]", "i", x)
    x = re.sub("[oòóɔɔ̀]", "o", x)
    x = re.sub("[uùúʊ]", "u", x)
    x = re.sub("[gɡ]", "g", x)
    x = re.sub("[lɫ]", "l", x)
    x = re.sub("[rɹ]", "r", x)
    x = re.sub("[æǽӕ]", "æ", x)
    x = re.sub("[əɜʌΛ]", "ə", x)
    x = re.sub("ɝ", "ər", x)
    x = re.sub("ʤ", "dʒ", x)
    x = re.sub("ʧ", "tʃ", x)
    x = re.sub("[ːː]", "", x)

    x = re.sub("[^abcdefghijklmnopqrstuvwxyzæðŋəɹʃʒθˈˌ]", "", x)

    return x

def syllabify_ipa(x):

    # onsets
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋɹʃʒθ]"
    C2 = "[bfgkp]l|[bdfgktp]r|[dgptk]w|[bdfghklmnpstvzʒθ]j|s[kmnpt]"
    C3 = "s[kmpt]j|s[kp][lr]|s[ft]r|skw"

    # vowels
    V1 = "[aeiouæə]" # monophthongs
    V2 = "[aoə][iu]|ei|[eiu]ə" # diphthongs
    V3 = "([aeo]i|[aoə]u)ə" # triphthongs

    # phoneme segmentation
    x = normalize(x)
    x = re.sub(f" ?({V3}|{V2}|{V1})", r" _\1_", x)

    # onset maximalization
    x = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", x)

    # coda concatenation
    f = lambda m: m.group(1) + "_" + m.group(2).replace(' ', '')
    x = re.sub("(_[^ ˈˌ]+)(( [^ _]+)+)(?=[ ˈˌ])", f, x)

    # post-processing
    x = re.sub(" ?[ˈˌ] ?", " ", x)
    x = x.strip()
    x = x.split(" ")

    return x

def syllabify_en(x):

    # onsets
    C1 = "[bcdgkprstw]h|([bcdfghjklmnpqrstvwxyz])\\2?"
    C2 = "[bcfgkp]l|[bcdfgktp]r|[cdgptk]w|s[ckmnpqt]"
    C3 = "s[ckp][lr]|s[ft]r|skw"

    # vowels
    V = "[aeiou]+|[aeou]y|y(?![aeou])"

    # phoneme segmentation
    x = normalize(x)
    x = re.sub(f" ?({V})", r" _\1_", x)

    # onset maximalization
    x = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", x)

    # coda concatenation
    f = lambda m: m.group(1) + "_" + m.group(2).replace(' ', '')
    x = re.sub("(_[^ ˈˌ]+)(( [^ _]+)+)(?=[ˈˌ ])", f, x)

    # post-processing
    x = x.strip()
    x = x.split(" ")

    return x

def syllabify_enko(x):

    s, y = [], []

    for i, p in enumerate(x):

        j = i + 1
        # print(y, s, "<-", p)

        if p == "$":
            y.append(s)
            break

        if p in _EN_C:

            if s and s[-1] + p in ("dʒ", "tʃ"):
                s[-1] += p
                continue

            if len(s) == 1 and p == "j":
                s[0] += p
                continue

            if len(s) in (1, 3):
                y.append(s)
                s = []

            if len(s) == 2:

                k = False

                if p not in "bklmnprŋ":
                    k = True

                if j < len(x) and x[j] in _EN_V + "jlr":
                    k = True

                if k:
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

    return y

def combine_with_y(x):

    return {a:b for a, b in zip("aeouæə", "ㅑㅖㅛㅠㅒㅕ")}.get(x, x)

def combine_with_w(x):

    return {a:b for a, b in zip("aeioæə", "ㅘㅞㅟㅝㅙㅝ")}.get(x, x)

def ipa_to_han(en) : # IPA to Hangeul syllables

    en = syllabify_enko(en)
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

        if len(s) > 1:

            if s[0] == "":
                s[0] = "ㅇ"
            if s[0][-1:] == "j":
                s[0] = "ㅇ" if s[0] == "j" else s[0][:-1]
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

        if len(s) == 2:

            if j < len(en) and en[j][0] == "l":
                s.append("ㄹ")

        if len(s) == 3:

            if s[2] == "k":
                s[2] = "ㄱ"
            if s[2] == "p":
                s[2] = "ㅂ"
            if s[2] == "t":
                s[2] = "ㅅ"

        s = [_ENKO.get(p, p) for p in s]
        en[i] = "".join(s)

    ko = "".join(jamofy.jamo_to_syl(s) for s in en)

    return ko

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: %s en|enko < filename")

    method = sys.argv[1]

    for line in sys.stdin:

        line = line.strip()
        a, b = line.split("\t")

        if method == "en":
            # print(*syllabify(b), sep = "\n")
            _a = syllabify_en(a)
            _b = syllabify_ipa(b)
            if len(_a) != len(_b):
                continue
            print(a, b, _a, _b, sep = "\t")

        if method == "enko":
            print(a, b, ipa_to_han(b), sep = "\t")
