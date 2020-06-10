import sys
import re
import json

def json2tsv():
    pl = dict()
    cnt = 0
    
    with open(sys.argv[1]) as fo:
        names = sys.argv[2:]
        for line in fo:
            f = True
            jo = json.loads(line)
            cnt += 1
            values = []
            for x in names:
                if x not in line:
                    f = False
                    break
            if not f:
                continue
            f = True
            for x in names:
                y = jo[x]
                y = re.sub("\s+", " ", y)
                y = y.strip()
                if y == "":
                    f = False
                    break
                values.append(y)
            if not f:
                continue
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
