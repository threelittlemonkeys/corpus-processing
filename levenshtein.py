import sys

def edit_distance(a, b, Wd = 1, Wi = 1, Ws = 1, Wt = 0, thesaurus = {}, backtrace = False, verbose = False):

    # initialize distance matrix

    za = len(a) + 1
    zb = len(b) + 1
    m = [[0 for _ in range(zb)] for _ in range(za)]
    bt = []

    for i in range(za):
        m[i][0] = i
    for j in range(zb):
        m[0][j] = j

    # compute Damerau-Levenshtein distances

    for i in range(1, za):
        for j in range(1, zb):

            m[i][j] = min(
                m[i - 1][j] + Wd, # deletion
                m[i][j - 1] + Wi, # insertion
                m[i - 1][j - 1] + (not in_thesaurus(a[i - 1], b[j - 1], thesaurus)) * Ws # substitution
            )

            # transposition

            if i > 1 and j > 1 and Wt \
            and in_thesaurus(a[i - 1], b[j - 2], thesaurus) \
            and in_thesaurus(a[i - 2], b[j - 1], thesaurus):
                m[i][j] = min(m[i][j], m[i - 2][j - 2] + Wt)

    if backtrace:

        bt = backtrace_edit_distance(a, b, m, thesaurus)

    if verbose:

        print("edit_distance_matrix =")
        print_edit_distance_matrix(a, b, m)
        # print_edit_distance_matrix_colored(a, b, m, bt)
        print()

        print("edit_distance_backtrace =")
        for e in bt:
            print(e)
        print()

    return m[-1][-1], bt

def in_thesaurus(a, b, thesaurus):

    if a in thesaurus and b in thesaurus[a]:
        return True

    if b in thesaurus and a in thesaurus[b]:
        return True

    return a == b

def print_edit_distance_matrix(a, b, m):

    print("  ".join([" ", " "] + list(b)))

    for i in range(len(a) + 1):
        c = a[i - 1] if i else " "
        print(" ".join([c, *[f"{j:2d}" for j in m[i]]]))

def print_edit_distance_matrix_colored(a, b, m, bt):

    _m = []
    yl = lambda x: f"\033[38;5;226m{x}\033[0m"

    for i in range(len(a) + 1):
        c = a[i - 1] if i else " "
        _m.append([c, *[f"{j:2d}" for j in m[i]]])

    _m[0][1] = yl(_m[0][1])
    for i, j, *_, in bt: # highlight color
        _m[i][j + 1] = yl(_m[i][j + 1])

    print("  ".join([" ", " "] + list(b)))
    print("\n".join(" ".join(xs) for xs in _m))

def backtrace_edit_distance(a, b, m, thesaurus):

    x, y = len(a), len(b)
    bt = []
    ed = ((1, 1), (1, 0), (0, 1))
    op = ("substitute", "delete", "insert", "transpose")

    while x > 0 or y > 0:

        d, i = min([
            (m[x - a][y - b], i)
            for i, (a, b) in enumerate(ed)
            if x >= a and y >= b
        ])

        if d == m[x][y]:
            o = None if in_thesaurus(a[x - 1], b[y - 1], thesaurus) else op[-1]
        else:
            o = op[i if not bt or op[-1] != bt[-1][-1] else -1]

        bt.append([x, y, m[x][y], o])
        x -= ed[i][0]
        y -= ed[i][1]

    return bt[::-1]

if __name__ == "__main__":

    a = "money"
    b = "donkeys"

    ed, _ = edit_distance(a, b, backtrace = True, verbose = True)
    print("edit_distance =", ed)
