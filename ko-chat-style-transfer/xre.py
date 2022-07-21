import sys
import re
import random
from xre_utils import *

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
