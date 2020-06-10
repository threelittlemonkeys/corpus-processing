import sys
import re
from collections import defaultdict

HWK = "｡｢｣､･ｳﾞｶﾞｷﾞｸﾞｹﾞｺﾞｻﾞｼﾞｽﾞｾﾞｿﾞﾀﾞﾁﾞﾂﾞﾃﾞﾄﾞﾊﾞﾋﾞﾌﾞﾍﾞﾎﾞﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝﾞﾟ" # half width Katakana
FWK = "。「」、・ヴガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナ>ニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜" # full width Katakana
H2FK = {h: f for h, f in zip(HWK, FWK)}

def clean_corpus(filename, options):
    fo = open(filename)
    verbose = "v" in options

    for line in fo:
        raw = line.strip()

        # control characters
        line = re.sub("[\u0000-\u001F\u007F\u0080-\u009F]+", " ", line)

        # whitespace characters
        line = re.sub("[\u0020\u00A0\u2000-\u200B\u202F\u205F\u3000]+", " ", line)

        # private use area
        line = re.sub("[\uE000-\uF8FF]", " ", line)

        # byte order marks
        line = re.sub("[\uFEFF\uFFFE]", " ", line)

        # full width characters
        line = "".join(chr(ord(c) - 0xFEE0) if "\uFF01" <= c <= "\uFF5E" else c for c in line)

        # half width characters
        i, _line = 0, ""
        while i < len(line):
            k = True
            for j in (2, 1):
                if line[i:i + j] in HWK:
                    _line += H2FK[line[i:i + j]]
                    k = False
                    i += j
                    break
            if k:
                _line += line[i]
                i += 1
        line = _line

        line = re.sub(" {2,}", " ", line)
        line = line.strip()

        if not verbose:
            print(line)
        elif raw != line:
            print(raw)
            print(line)

    fo.close()

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: %s filename [-v]" % sys.argv[0])

    options = "" if len(sys.argv) == 2 else sys.argv[2]
    clean_corpus(sys.argv[1], options)
