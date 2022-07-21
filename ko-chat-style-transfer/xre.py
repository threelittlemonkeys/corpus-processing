import sys
import re
import random
from xre_utils import *

RE_SYM_DEF = re.compile("^<([^ >]+)> = (.+)$")
RE_SYM_CONCAT = re.compile("^<([^ >]+)> = (<[^ >]+>(?: \+ <[^ >]+>)+)$")

RE_CHARSET = re.compile(r"\[[^^]([^]]|\\])*\]")
RE_GROUP = re.compile(r"\(([^)]|\\\))*\)")
RE_BACKREF = re.compile(r"(?!>\\)\\[0-9]+")

class xre_object():

    def __init__(self):

        self.pt = None
        self.pt_groups = None
        self.repl = None

        self._idx = None
        self._args = None

def read(filename):
    do = {}
    fo = open(filename)
    syms = {}

    for ln, line in enumerate(fo, 1):

        # preprocessing

        line = re.sub("#.*", "", line)
        line = re.sub("  +", " ", line)
        line = re.sub(" *\t *", "\t", line)
        line = line.strip()

        if line == "":
            continue
        if line == "<EOF>":
            break

        # symbols

        m = RE_SYM_DEF.search(line)
        if m:
            k, v = m.groups()
            syms[k] = v
            continue

        m = RE_SYM_CONCAT.search(line)
        if m:
            k, vs = m.groups()
            v = "(?:%s)" % "|".join([syms[v[1:-1]] for v in vs.split(" + ")])
            syms[k] = v
            continue

        try:
            item = re.sub("<(.+?)>", lambda x: "(?:%s)" % syms[x.group(1)], line)
        except:
            sys.exit("Error: unknown symbol at line %d" % ln)

        # load dictionary items

        try:
            x, y = item.split("\t")
        except:
            sys.exit("Error: invalid format at line %d" % ln)

        x = re.compile(x)

        if x not in do:
            do[x] = []
        elif y in do[x]:
            sys.exit("Error: item already exists at line %d" % ln)
        do[x].append((y, line))

    fo.close()
    return do

def find_groups(txt):

    k = 1
    depth = 0
    esc = False
    charset = False
    groups = []

    for i, c in enumerate(txt):
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == "[":
            charset = True
        elif c == "]":
            if not charset:
                return False
            charset = False
        elif charset:
            pass
        elif c == "(":
            depth += 1
            if depth == k:
                groups.append([[i + 1]])
        elif c == "|":
            if depth == 0 != k:
                groups = [[[0]]]
                k = 0
            if depth == k:
                groups[-1][-1].append(i)
            groups[-1].append([i + 1])
        elif c == ")":
            if depth == 0:
                return False
            if depth == k:
                groups[-1][-1].append(i)
            depth -= 1

    if k == 0:
        groups = groups[0]
        groups[-1].append(len(txt))
    elif groups and len(groups[-1][-1]) != 2:
        return False

    return groups # [[txt[i:j] for i, j in x] for x in groups]

def sub(pt, repl, txt):
    ro = xre_object()

    # pattern

    ro.pt = re.compile(pt) if type(pt) == str else pt
    ro.pt_groups = find_groups(ro.pt.pattern)

    # replacement

    repl = RE_CHARSET.sub(
        lambda x: random.choice(x.group()[1:-1]),
        repl
    )

    while RE_GROUP.search(repl):
        repl = RE_GROUP.sub(
            lambda x: random.choice(x.group()[1:-1].split("|")),
            repl
        )

    ro.repl = repl

    # substitution

    def sub_x(xm):
        xs = xm.groups()
        y = ro.repl

        def sub_y(ym, func):
            ro._idx = int(ym.group(1)) - 1
            ro._args = (xs[ro._idx], *ym.groups()[1:])
            return func(ro)

        for pt, func in xre_utils:
            y = pt.sub(lambda m: sub_y(m, func), y)

        y = RE_BACKREF.sub(lambda m: xs[int(m.group()[1:]) - 1], y)

        return y

    return ro.pt.sub(sub_x, txt)

