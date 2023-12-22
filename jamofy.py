import sys
import re
from syllabify import *

_IDX_TO_HIC = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # Hangeul initial consonants
_IDX_TO_HMV = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # Hangeul medial vowels
_IDX_TO_HFC = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # Hangeul final consonants

_HIC_TO_IDX = {c: i for i, c in enumerate(_IDX_TO_HIC)}
_HMV_TO_IDX = {c: i for i, c in enumerate(_IDX_TO_HMV)}
_HFC_TO_IDX = {c: i for i, c in enumerate(_IDX_TO_HFC[1:], 1)}

def syl_to_jamo(x): # decompose Hangeul syllables into jamo

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

        o += _IDX_TO_HIC[i]
        o += _IDX_TO_HMV[m]
        if f:
            o += _IDX_TO_HFC[f]

    return o

def jamo_to_syl(x) : # compose Hangeul jamo to syllables

    x += "\n"
    y, s = [], []

    for i, c in enumerate(x):

        if len(s) == 0 and c in _HIC_TO_IDX:
            s.append(c)
        elif len(s) == 1:
            if c in _HMV_TO_IDX:
                s.append(c)
            else:
                y.append(s[0])
                s = [c]
        elif len(s) == 2 and c in _HFC_TO_IDX:
            j = i + 1
            if j < len(x) and x[j] in _HMV_TO_IDX:
                y.append(s)
                s = [c]
            else:
                y.append(s + [c])
                s = []
        else:
            if s:
                y.append(s)
                s = []
            y.append(c)

    y = "".join([s if type(s) == str else chr(0xAC00
        + _HIC_TO_IDX[s[0]] * 21 * 28
        + _HMV_TO_IDX[s[1]] * 28
        + (_HFC_TO_IDX[s[2]] if len(s) == 3 else 0))
        for s in y[:-1]
    ])

    return y

if __name__ == "__main__":

    '''
    a = "정 참판 양반댁 규수 큰 교자 타고 혼례 치른 날"
    b = syl_to_jamo(a)
    c = jamo_to_syl(b)

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
            print(syl_to_jamo(line))
        if method == "j2s":
            print(jamo_to_syl(line))
