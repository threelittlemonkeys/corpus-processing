import sys
import difflib

if 4 < len(sys.argv) < 3 or len(sys.argv) == 4 and sys.argv[3] != "-v":
    sys.exit("Usage: %s filename1 filename2 [-v]" % sys.argv[0])

verbose = (len(sys.argv) == 4)

with open(sys.argv[1]) as fa, open(sys.argv[2]) as fb:
    ln = 0
    while True:
        a = fa.readline()
        b = fb.readline()
        if not a or not b:
            break
        ln += 1

        c = difflib.Differ()
        d = c.compare(a, b)

        i = 0
        diffs = []
        for j, k in enumerate(d):
            if k[:2] == "  ":
                continue
            if j != i + 1:
                diffs.append(["", "", ""])
            i = j
            if k[0] == "-":
                diffs[-1][0] += k[2:]
            if k[0] == "+":
                diffs[-1][1] += k[2:]
            if k[0] == "?":
                diffs[-1][2] += k[2:]

        diffs = [x for x in diffs for x in x if x]
        if not diffs:
            continue

        if verbose:
            print(ln, a, sep = "\t", end = "")
            print(ln, b, sep = "\t", end = "")
            print(ln, diffs, sep = "\t")
            print()
        else:
            for diff in diffs:
                print(ln, diff, sep = "\t")
