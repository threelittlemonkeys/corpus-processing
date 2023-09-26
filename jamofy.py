import sys
import re

_i2I = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
_i2M = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
_i2F = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants

_I2i = {c: i for i, c in enumerate(_i2I)}
_M2i = {c: i for i, c in enumerate(_i2M)}
_F2i = {c: i for i, c in enumerate(_i2F[1:], 1)}

def s2j(x): # decompose Hangeul syllables into jamo

    o = ""

    for c in x:

        u = ord(c)
        if u < 0xAC00 or u > 0xD7A3: # if not Hangeul syllable
            o += c
            continue

        u -= 0xAC00
        f = u % 28 # final consonant
        m = u // 28 % 21 # medial vowel
        i = u // 28 // 21 # initial consonant

        o += _i2I[i]
        o += _i2M[m]
        if f:
            o += _i2F[f]

    return o

def j2s(x) : # compose Hangeul jamo to syllables

    x += "\n"
    o, s = [], []

    for i, c in enumerate(x):

        if len(s) == 0 and c in _I2i:
            s.append(c)
        elif len(s) == 1:
            if c in _M2i:
                s.append(c)
            else:
                o.append(s[0]) # o.append(s + ["ㅡ"])
                s = [c]
        elif len(s) == 2 and c in _F2i:
            j = i + 1
            if j < len(x) and x[j] in _M2i:
                o.append(s)
                s = [c]
            else:
                o.append(s + [c])
                s = []
        else:
            if s:
                o.append(s)
                s = []
            o.append(c)

    print(o)
    o = "".join([s if type(s) == str else chr(0xAC00
        + _I2i[s[0]] * 21 * 28
        + _M2i[s[1]] * 28
        + (_F2i[s[2]] if len(s) == 3 else 0))
        for s in o[:-1]
    ])

    return o

if __name__ == "__main__":

    '''
    a = "정 참판 양반댁 규수 큰 교자 타고 혼례 치른 날"
    b = s2j(a)
    c = j2s(b)

    print(a)
    print(b)
    print(c)
    '''

    if len(sys.argv) != 2:
        sys.exit("Usage: %s s2j|j2s < filename")

    method = sys.argv[1]

    for line in sys.stdin:
        line = line.strip()
        if method == "s2j":
            print(s2j(line))
        if method == "j2s":
            print(j2s(line))
