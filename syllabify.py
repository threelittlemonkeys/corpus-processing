import sys
import re
import jamofy

# sonority sequencing principle (SSP)
# sonority hierarchy
# vowels > glides > liquids > nasals > fricatives > affricates > plosives

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
    x = re.sub("[əɜʌ]", "ə", x)
    x = re.sub("ɝ", "ər", x)
    x = re.sub("ɪr", "ɪər", x)
    x = re.sub("ʤ", "dʒ", x)
    x = re.sub("ʧ", "tʃ", x)
    x = re.sub("ː", "", x)

    x = re.sub("(?=<[^d]ʒ)j(?=ə)", "", x)
    x = re.sub("(?=<[^t]ʃ)j(?=ə)", "", x)

    x = re.sub("[^abcdefghijklmnopqrstuvwxyzæðŋəʃʒθˈˌ.]", "", x)

    return x

def concat_coda(m):
    return m.group(1) + "_" + m.group(2).replace(' ', '')

def syllabify_ipa(x):

    # onsets
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bfgkps]l|[bdfgkptθ]r|[dgkst]w|[bdfghklmnpstvzʒθ]j|dʒj|s[kmnpt]"
    C3 = "s[kmpt]j|s[kp][lr]|s[ft]r|skw"

    # vowels
    V1 = "[aeiouæə]" # monophthongs
    V2 = "[aoə][iu]|ei|[eiu]ə" # diphthongs
    V3 = "[aeo]iə|[aoə]uə" # triphthongs

    # phoneme segmentation
    x = normalize(x)
    x = re.sub(f" ?({V2}|{V1})", r" _\1_", x)

    # onset maximalization
    x = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", x)

    # coda concatenation
    x = re.sub("(_[^ ˈˌ.]+)(( [^ _]+)+)(?=[ ˈˌ.])", concat_coda, x)

    # post-processing
    x = re.sub(" ?[ˈˌ] ?", " ", x)
    x = x.strip()
    x = [x.split("_") for x in x.split(" ")]

    return x

def syllabify_en(x):

    # onsets
    C1 = "[bcdgkprstw]h|([bdfgjklmnprstxvz])\\2|[bcdfghjklmnpqrstvwxyz]"
    C2 = "[bcfgkps]l|[bcdfgkpt]r|[cdgkpst]w|s[cfkmnpqt]"
    C3 = "s[ckp][lr]|s[ft]r|skw"

    # vowels
    V = "[aeou]y|[aeiou]+|y(?![aeou])"

    # phoneme segmentation
    x = normalize(x)
    x = re.sub(f" ?({V})", r" _\1_", x)

    # onset maximalization
    x = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", x)

    # coda concatenation
    x = re.sub("(_[^ ˈˌ]+)(( [^ _]+)+)(?=[ ˈˌ])", concat_coda, x)

    # post-processing
    x = x.strip()
    x = [x.split("_") for x in x.split(" ")]

    return x

def syllabify_enko(_en, _ipa):

    # consonants
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bdfghklmnpstvzʒθ]j|dʒj|[gk]w|dz|ts"

    _ko = []

    for i, x in enumerate(_ipa):

        try:
            o, n, c = x
        except: # invalid syllable
            return None

        y = []

        # onset

        o = re.findall(f"{C2}|{C1}", o)

        if not o:
            y.append([""])

        for p in o:
            if p == "l":
                e = y[-1] if y else _ko[-1][-1] if _ko else None
                if e and len(e) != 3:
                    if len(e) == 1:
                        e.append("")
                    e.append("l")
            y.append([p])

        # nucleus

        if (c or i < len(_ipa) - 1) and n == "ou":
            n = "o"

        for p in n:
            if len(y[-1]) == 2:
                y.append([""])
            y[-1].append(p)

        # coda

        c = re.findall(f"{C2}|{C1}", c)

        for p in c:
            if len(y[-1]) == 3 and y[-1][-1] == "" and p in ("l", "m", "n"):
                y[-1][-1] = p
                continue
            if len(y[-1]) != 2 \
            or p not in ("b", "k", "l", "m", "n", "p", "r", "ŋ"):
                y.append([])
            if p == "r":
                p = ""
            y[-1].append(p)

        _ko.append(y)

    ko = ipa_to_hangeul(_en, _ko)

    return ko

def ipa_to_hangeul(_en, _ko) : # IPA to Hangeul syllables

    _ENKO = {
        **{a: b for a, b in zip(
        "abdefghiklmnoprstuvzæðŋəʃʒθ",
        "ㅏㅂㄷㅔㅍㄱㅎㅣㅋㄹㅁㄴㅗㅍㄹㅅㅌㅜㅂㅈㅐㄷㅇㅓㅅㅈㅅ")},
        **{a: b for a, b in zip(
        ("dz", "dʒ", "ts", "tʃ"),
        ("ㅈ", "ㅈ", "ㅊ", "ㅊ"))},
        **{a: b for a, b in zip(
        ("ja", "je", "ji", "jo", "ju", "jæ", "jə"),
        ("ㅑ", "ㅖ", "ㅣ", "ㅛ", "ㅠ", "ㅒ", "ㅕ"))},
        **{a: b for a, b in zip(
        ("wa", "we", "wi", "wo", "wu", "wæ", "wə"),
        ("ㅘ", "ㅞ", "ㅟ", "ㅝ", "ㅜ", "ㅙ", "ㅝ"))},
    }

    ko = ""

    for xs in _ko:
        for x in xs:

            if len(x) == 1:
                x.append("")
            if x[0][-1:] in ("j", "w"):
                x[0], j = x[0][:-1], x[0][-1]
                x[1] = j + x[1]
            if x[0] == "ʃ" and x[1]:
                x[1] = "j" + x[1]
            if x[0] == "":
                x[0] = "ㅇ"
            if x[1] == "":
                x[1] = "ㅣ" if x[0][-1] in ("ʃ", "ʒ") else "ㅡ"

            x = [_ENKO.get(p, p) for p in x]

            if len(x) == 3:
                if x[2] == "ㅋ":
                    x[2] = "ㄱ"
                if x[2] == "ㅌ":
                    x[2] = "ㅅ"
                if x[2] == "ㅍ":
                    x[2] = "ㅂ"

            ko += jamofy.jamo_to_syl(x)

    return ko

if __name__ == "__main__":

    for line in sys.stdin:

        line = line.strip()
        en, ipa = line.split("\t")

        _en = syllabify_en(en)
        _ipa = syllabify_ipa(ipa)
        _ko = syllabify_enko(_en, _ipa)

        if _ko == None:
            print(en, ipa, sep = "\t")
            continue

        _en = ".".join("".join(x) for x in _en)
        _ipa = ".".join("".join(x) for x in _ipa)

        print(en, ipa, _en, _ipa, _ko, sep = "\t")
