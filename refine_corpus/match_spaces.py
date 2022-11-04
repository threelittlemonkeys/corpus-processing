import sys
import re

flag = sys.argv[1]
assert flag in ("diff", "sent")

def normalize(txt):
    return txt.replace(" ", "")

for line in sys.stdin:
    src, tgt = line.strip().split("\t")

    xws = []
    yws = []

    for m in re.finditer("[A-Za-z][A-Za-z ]+[A-Za-z]", src):
        xws.append((m.group(), m.start()))

    for m in re.finditer("[A-Za-z][A-Za-z ]+[A-Za-z]", tgt):
        yws.append((m.group(), m.start()))


    zws = []

    for x in xws:
        for y in yws:
            if x[0] != y[0] and normalize(x[0]) == normalize(y[0]):
                zws.append((x, y))
                break

    if not zws:
        if flag == "sent":
            print(line, end = "")
        continue

    kx = 0
    ky = 0

    for (xw, xi), (yw, yi) in zws:

        if len(xw) > len(yw):
            tgt = tgt[:yi + ky] + xw + tgt[yi + len(yw) + ky:]
            ky += len(xw) - len(yw)

        if len(xw) < len(yw):
            src = src[:xi + kx] + yw + src[xi + len(xw) + kx:]
            kx += len(yw) - len(xw)

    if flag == "diff":
        for (xw, xi), (yw, yi) in zws:
            print((xw, yw))

    '''
    print(line, end = "", file = sys.stderr)
    print(src, tgt, sep = "\t", file = sys.stderr)
    print(file = sys.stderr)
    '''

    if flag == "sent":
        print(src, tgt, sep = "\t")
