import re

RE_MODIFY_FC = re.compile(r"\{([0-9]+):MODIFY_FC:([ㄱ-ㅎ]?)\}")
RE_REMOVE_FC = re.compile(r"\{([0-9]+):REMOVE_FC\}")
RE_SUB = re.compile(r"\{([0-9]+):SUB:((?:[^}]|\\\})+(?:\|(?:[^}]|\\\})*)+)\}")

I2FC = [""] + list("ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")
FC2I = {f: i for i, f in enumerate(I2FC)}

def modify_fc(ro):
    x, y = ro._args
    u = ord(x[-1])
    if u < 0xAC00 or u > 0xD7A3:
        return x
    f = (u - 0xAC00) % 28
    if not (I2FC[f] == "ㅄ" and y == "ㅅ"):
        u = u - f + FC2I[y]
    return x[:-1] + chr(u)

def remove_fc(ro):
    x, = ro._args
    u = ord(x[-1])
    if u < 0xAC00 or u > 0xD7A3:
        return x
    f = (u - 0xAC00) % 28
    u -= f
    if I2FC[f] == "ㄶ":
        u += FC2I["ㄴ"]
    if I2FC[f] == "ㅀ":
        u += FC2I["ㄹ"]
    if I2FC[f] == "ㅄ":
        u += FC2I["ㅂ"]
    return x[:-1] + chr(u)

def sub(ro):
    c = ro._args[0]
    xs = [ro.pt.pattern[i:j] for i, j in ro.pt_groups[ro._idx]]
    ys = ro._args[1].split("|")
    return next(y for x, y in zip(xs, ys) if re.match(x, c))

xre_utils = [
    (RE_MODIFY_FC, modify_fc),
    (RE_REMOVE_FC, remove_fc),
    (RE_SUB, sub),
]
