import sys
import re
import json

def json2tsv():
    pl = dict()
    cnt = 0

    with open(sys.argv[1]) as fo:
        names = sys.argv[2:]
        for line in fo:
            jo = json.loads(line)
            cnt += 1
            values = []
            for x in names:
                if x in jo:
                    y = jo[x]
                    y = re.sub("\s+", " ", y)
                    y = y.strip()
                else:
                    y = ""
                values.append(y)
            line = "\t".join(values)
            pl[line] = True

    for line in pl:
        print(line)

    sys.stderr.write("%d in total\n" % cnt)
    sys.stderr.write("%d uniq \n" % len(pl))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: %s filename name1 ...")
    json2tsv()
