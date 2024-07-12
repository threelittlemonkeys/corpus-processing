import sys

def edit_distance(a, b, Wd = 1, Wi = 1, Ws = 1, Wt = 1, verbose = False): # Levenshtein distance

    # initialize distance matrix

    za = len(a) + 1
    zb = len(b) + 1

    m = [[0 for _ in range(zb)] for _ in range(za)]

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
                m[i - 1][j - 1] + (a[i - 1] != b[j - 1]) * Ws # substitution
            )

            if not (i and j and Wt):
                continue

            if a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]: # transposition
                m[i][j] = min(m[i][j], m[i - 2][j - 2] + Wt)

    if verbose:
        backtrace_edit_distance(a, b, m)

    return m[-1][-1]

def backtrace_edit_distance(a, b, m):

    # edit distance matrix

    print("  ".join([" ", " "] + list(b)))

    for i in range(len(a) + 1):
        c = a[i - 1] if i else " "
        print(f"{c} " + " ".join(f"{j:2d}" for j in m[i]))

    # backtrace

    x, y = len(a), len(b)
    bt = []
    ed = ((1, 1), (1, 0), (0, 1))
    op = ("substitution", "deletion", "insertion", "transposition")

    while x > 0 or y > 0:

        d, i = min([
            (m[x - a][y - b], i)
            for i, (a, b) in enumerate(ed)
            if x >= a and y >= b
        ])

        if d == m[x][y]:
            o = op[-1] if a[x - 1] != b[y - 1] else "same"
        else:
            o = op[i if not bt or op[-1] != bt[-1][-1] else -1]

        bt.append([x, y, m[x][y], o])
        x -= ed[i][0]
        y -= ed[i][1]

    for e in reversed(bt):
        print(e)

if __name__ == "__main__":

    a = "money"
    b = "donkey"

    a = "abc"
    b = "bac"

    ed = edit_distance(a, b, verbose = True)
    print(ed)
