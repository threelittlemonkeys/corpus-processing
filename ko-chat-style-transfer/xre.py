import sys
import re
import random
from xre_utils import *

RE_CHARSET = re.compile(r"\[[^^]([^]]|\\])*\]")
RE_GROUP = re.compile(r"\(([^)]|\\\))*\)")

class xre_object():

    def __init__(self):

        self.pt = None
        self.pt_groups = None
        self.repl = None
        self.txt = None
        self.txt_groups = None

        self._match = None
        self._idx = None
        self._arg = None

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

    if type(pt) == str:
        pt = re.compile(pt)
    pt_groups = find_groups(pt.pattern)

    repl = RE_CHARSET.sub(
        lambda x: random.choice(x.group()[1:-1]),
        repl
    )

    while RE_GROUP.search(repl):
        repl = RE_GROUP.sub(
            lambda x: random.choice(x.group()[1:-1].split("|")),
            repl
        )

    xs = []
    for m in pt.finditer(txt):
        for i, x in enumerate(m.groups(), 1):
            if not x:
                continue
            if xs and m.span(i)[1] <= xs[-1][1][1]:
                continue
            xs.append((x, m.span(i)))

    ro = xre_object()
    ro.pt = pt
    ro.pt_groups = pt_groups
    ro.repl = repl
    ro.txt = txt
    ro.txt_groups = [x[0] for x in xs]

    def proc(m, func):
        ro._match = m
        ro._idx = int(m.group(1)) - 1
        ro._arg = ro.txt_groups[ro._idx]
        return func(ro)

    for pt, func in xre_utils:
        ro.repl = pt.sub(lambda m: proc(m, func), ro.repl)

    return ro.pt.sub(ro.repl, ro.txt)
