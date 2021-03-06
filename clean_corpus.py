import sys
import re

HWK = "｡ ｢ ｣ ､ ･ ｳﾞ ｶﾞ ｷﾞ ｸﾞ ｹﾞ ｺﾞ ｻﾞ ｼﾞ ｽﾞ ｾﾞ ｿﾞ ﾀﾞ ﾁﾞ ﾂﾞ ﾃﾞ ﾄﾞ ﾊﾞ ﾋﾞ ﾌﾞ ﾍﾞ ﾎﾞ ﾊﾟ ﾋﾟ ﾌﾟ ﾍﾟ ﾎﾟ ｦ ｧ ｨ ｩ ｪ ｫ ｬ ｭ ｮ ｯ ｰ ｱ ｲ ｳ ｴ ｵ ｶ ｷ ｸ ｹ ｺ ｻ ｼ ｽ ｾ ｿ ﾀ ﾁ ﾂ ﾃ ﾄ ﾅ ﾆ ﾇ ﾈ ﾉ ﾊ ﾋ ﾌ ﾍ ﾎ ﾏ ﾐ ﾑ ﾒ ﾓ ﾔ ﾕ ﾖ ﾗ ﾘ ﾙ ﾚ ﾛ ﾜ ﾝ ﾞ ﾟ".split(" ") # half width Katakana
FWK = "。「」、・ヴガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜" # full width Katakana
H2FWK = {h: f for h, f in zip(HWK, FWK)}

def clean_line(line):

    # control characters
    line = re.sub("[\u0000-\u0006\u0008-\u001F\u007F\u0080-\u009F]+", " ", line)

    # whitespace characters
    line = re.sub("[\u0007\u0020\u00A0\u2000-\u200B\u202F\u205F\u3000]+", " ", line)

    # private use area
    line = re.sub("[\uE000-\uF8FF]+", " ", line)

    # byte order marks
    line = re.sub("[\uFEFF\uFFFE]+", " ", line)

    # full width characters
    line = "".join(chr(ord(c) - 0xFEE0) if "\uFF01" <= c <= "\uFF5E" else c for c in line)

    # half width characters
    i, _line = 0, ""
    while i < len(line):
        k = True
        for j in (2, 1):
            if line[i:i + j] in H2FWK:
                _line += H2FWK[line[i:i + j]]
                k = False
                i += j
                break
        if k:
            _line += line[i]
            i += 1
    line = _line

    # remove repetitive whitespace characters
    line = re.sub(" {2,}", " ", line)
    line = line.strip()

    return line

def clean_corpus(filename, options):
    fo = open(filename)
    bitext = "b" in options
    verbose = "v" in options

    for line in fo:
        raw = line.strip()
        line = clean_line(line)

        if not verbose:
            print(line)
        elif raw != line:
            print(raw)
            print(line)

    fo.close()

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: %s filename [-bv]" % sys.argv[0])

    options = "" if len(sys.argv) == 2 else sys.argv[2]
    clean_corpus(sys.argv[1], options)
