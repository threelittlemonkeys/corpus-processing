import sys
import re
from collections import defaultdict

HW_KATAKANA = "｡ ｢ ｣ ､ ･ ｳﾞ ｶﾞ ｷﾞ ｸﾞ ｹﾞ ｺﾞ ｻﾞ ｼﾞ ｽﾞ ｾﾞ ｿﾞ ﾀﾞ ﾁﾞ ﾂﾞ ﾃﾞ ﾄﾞ ﾊﾞ ﾋﾞ ﾌﾞ ﾍﾞ ﾎﾞ ﾊﾟ ﾋﾟ ﾌﾟ ﾍﾟ ﾎﾟ ｦ ｧ ｨ ｩ ｪ ｫ ｬ ｭ ｮ ｯ ｰ ｱ ｲ ｳ ｴ ｵ ｶ ｷ ｸ ｹ ｺ ｻ ｼ ｽ ｾ ｿ ﾀ ﾁ ﾂ ﾃ ﾄ ﾅ ﾆ ﾇ ﾈ ﾉ ﾊ ﾋ ﾌ ﾍ ﾎ ﾏ ﾐ ﾑ ﾒ ﾓ ﾔ ﾕ ﾖ ﾗ ﾘ ﾙ ﾚ ﾛ ﾜ ﾝ ﾞ ﾟ".split(" ")
FW_KATAKANA = "。 「 」 、 ・ ヴ ガ ギ グ ゲ ゴ ザ ジ ズ ゼ ゾ ダ ヂ ヅ デ ド バ ビ ブ ベ ボ パ ピ プ ペ ポ ヲ ァ ィ ゥ ェ ォ ャ ュ ョ ッ ー ア イ ウ エ オ カ キ ク ケ コ サ シ ス セ ソ タ チ ツ テ ト ナ >ニ ヌ ネ ノ ハ ヒ フ ヘ ホ マ ミ ム メ モ ヤ ユ ヨ ラ リ ル レ ロ ワ ン ゛ ゜".split(" ")
HW_TO_FW_KATAKANA = {h: f for h, f in zip(HW_KATAKANA, FW_KATAKANA)}

def clean_corpus(filename, options):
    fo = open(filename)
    verbose = "v" in options

    for line in fo:
        raw = line.strip()

        # control characters
        line = re.sub("[\u0000-\u001F\u007F\u0080-\u009F]", " ", line)

        # whitespace characters
        line = re.sub("[\u0020\u00A0\u2000-\u200B\u202F\u205F\u3000]", " ", line)

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
                if line[i:i + j] in HW_KATAKANA:
                    _line += HW_TO_FW_KATAKANA[line[i:i + j]]
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
