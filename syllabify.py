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
    x = re.sub("ʤ", "dʒ", x)
    x = re.sub("ʧ", "tʃ", x)
    x = re.sub("[ːː]", "", x)

    x = re.sub("[^abcdefghijklmnopqrstuvwxyzæðŋəʃʒθˈˌ]", "", x)

    return x

def concat_coda(m):
    return m.group(1) + "_" + m.group(2).replace(' ', '')

def syllabify_ipa(x):

    # onsets
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bfgkps]l|[bdfgkptθ]r|[dgkst]w|[bdfghklmnpstvzʒθ]j|s[kmnpt]"
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
    x = re.sub("(_[^ ˈˌ]+)(( [^ _]+)+)(?=[ ˈˌ])", concat_coda, x)

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
    C2 = "[bdfghklmnpstvzʒθ]j|[gk]w|dz|ts"

    _ko = []

    for x in _ipa:

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
        for p in n:
            if len(y[-1]) == 2:
                y.append([""])
            y[-1].append(p)

        # coda
        c = re.findall(f"{C2}|{C1}", c)
        for p in c:
            if p == "r":
                continue
            if len(y[-1]) != 2:
                y.append([])
            y[-1].append(p)

        _ko.append(y)

    return ipa_to_hangeul(_en, _ko)

def combine_with_y(x):

    return {a:b for a, b in zip("aeouæə", "ㅑㅖㅛㅠㅒㅕ")}.get(x, x)

def combine_with_w(x):

    return {a:b for a, b in zip("aeioæə", "ㅘㅞㅟㅝㅙㅝ")}.get(x, x)

def ipa_to_hangeul(_en, _ko) : # IPA to Hangeul syllables

    _ENKO = {**{a: b for a, b in zip(
        "abdefghiklmnoprstuvzæðŋəʃʒθ",
        "ㅏㅂㄷㅔㅍㄱㅎㅣㅋㄹㅁㄴㅗㅍㄹㅅㅌㅜㅂㅈㅐㄷㅇㅓㅅㅈㅅ"
    )}}

    y = []

    for xs in _ko:
        for x in xs:
            print(x, [_ENKO.get(p, p) for p in x])

    print(y)
    return _ko

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

    for line in sys.stdin:

        line = line.strip()
        en, ipa = line.split("\t")

        _en = syllabify_en(en)
        _ipa = syllabify_ipa(ipa)
        _ko = syllabify_enko(_en, _ipa)

        if _ko == None:
            # print(en, ipa, sep = "\t")
            continue

        _en = ".".join("".join(x) for x in _en)
        _ipa = ".".join("".join(x) for x in _ipa)

        print(en, ipa, _en, _ipa, _ko, sep = "\t")
        print()
