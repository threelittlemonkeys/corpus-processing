import sys

def edit_distance(a, b, Wd = 1, Wi = 1, Ws = 1, Wt = 1, verbose = False): # Levenshtein distance
    # initialize distance matrix
    Za = len(a) + 1
    Zb = len(b) + 1
    M = [[0 for i in range(Zb)] for j in range(Za)]
    for i in range(Za):
        M[i][0] = i
    for j in range(Zb):
        M[0][j] = j

    # compute Damerau-Levenshtein distances
    for i in range(1, Za):
        for j in range(1, Zb):
            M[i][j] = min(
                M[i - 1][j] + Wd, # deletion
                M[i][j - 1] + Wi, # insertion
                M[i - 1][j - 1] + (a[i - 1] != b[j - 1]) * Ws # substitution
            )
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]: # transposition
                M[i][j] = min(M[i][j], M[i - 2][j - 2] + Wt)

    if verbose:
        backtrace_edit_distance(a, b, M)

    return M[-1][-1]

def backtrace_edit_distance(a, b, M):
    # print edit distance matrix
    for i in range(len(a) + 1):
        if i == 0:
            sys.stdout.write("      ")
            for j in range(len(b)):
                sys.stdout.write("%s  " % b[j])
            sys.stdout.write("\n  ")
        for j in range(len(b) + 1):
            if i > 0 and j == 0:
                sys.stdout.write("%s " % a[i - 1])
            sys.stdout.write("%2d " % M[i][j])
        sys.stdout.write("\n")

    # backtrace
    x, y = len(a), len(b)
    pl, bt = [], []
    ed = ((1, 1), (1, 0), (0, 1))
    op = ("sub", "del", "ins")
    while x > 0 or y > 0:
        d, i = min([(M[x - a][y - b], i) for i, (a, b) in enumerate(ed) if x >= a and y >= b])
        o = ("same" if a[x - 1] == b[y - 1] else "trans") if d == M[x][y] else op[i]
        bt.append((x, y, d, o))
        x -= ed[i][0]
        y -= ed[i][1]
    for e in reversed(bt):
        print(e)

if __name__ == "__main__":
    a = "snow white"
    b = "happy prince"
    print(edit_distance(a, b, verbose = True))
