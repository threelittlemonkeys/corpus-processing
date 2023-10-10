import re
from utils import *

def find_tables(html):

    pt = "<table>.*?</table>"

    tables = [
        (m.start(), m.group())
        for m in re.finditer(pt, html)
    ]

    return tables

def parse_table(html):

    rows = []
    spans = [{}, {}]

    for row_idx, row_txt in enumerate(re.findall("<tr>.*?</tr>", html)):

        if row_idx == len(rows):
            rows.append([])
        row = rows[row_idx]
        col_idx = 0

        for m in re.finditer("<td(.*?)>(.*?)</td>", row_txt):

            attr = m.group(1).strip()
            cols = m.group(2).strip()

            while col_idx < len(row):
                if len(row[col_idx]):
                    col_idx += 1
                else:
                    break
            else:
                row.append([])

            row[col_idx] += [
                col.strip()
                for col in re.split("(?i)<br ?/?>", cols)
            ]

            rowspan = row_idx + 1
            colspan = col_idx + 1

            for m in re.finditer("([^= ]+)=([^= ]+)", attr):

                name = m.group(1)
                value = m.group(2)

                if re.match("['\"]?[0-9]+['\"]$", value):
                    value = int(value[1:-1])
                if name == "rowspan":
                    rowspan += value - 1
                if name == "colspan":
                    colspan += value - 1

            rows += [[] for _ in range(rowspan - len(rows))]
            for i in range(row_idx, rowspan):

                rows[i] += [[] for _ in range(colspan - len(rows[i]))]
                for j in range(col_idx, colspan):

                    if i > row_idx or j > col_idx:
                        rows[i][j] = [None]
                        spans[0][(i, j)] = i > row_idx
                        spans[1][(i, j)] = j > col_idx

            col_idx += 1

    col_size = max(len(row) for row in rows)
    row_lens = [max(len(cols) for cols in row) for row in rows]

    rows = [
        [cols + [""] * (row_len - len(cols)) for cols in row]
        + [[""] * row_len] * (col_size - len(row))
        for row, row_len in zip(rows, row_lens)
    ]

    col_lens = [
        max([ulen(col) for cols in row for col in cols])
        for row in zip(*rows)
    ]

    return (rows, spans, col_lens)

def print_table(html, end = "\n"):

    rows, spans, col_lens = parse_table(html)
    border = "-" * (sum(col_lens) + (len(col_lens) - 1) * 3 + 4)
    blocks = [[border]]

    for row_idx, row in enumerate(rows):

        blocks += [[], [border]]
        points = [0]

        for cols in zip(*row):
            line = []
            for col_idx, (col, col_len) in enumerate(zip(cols, col_lens)):
                line.append(col if type(col) == str else "")
                line[-1] += " " * (col_len - ulen(col))
            blocks[-2].append(line)

        for col_idx, col in enumerate(blocks[-2][0]):

            p = points[-1] + ulen(col) + 3

            if spans[0].get((row_idx, col_idx)):
                blocks[-3][0] = "".join(
                    " " if points[-1] <= i < p else c
                    for i, c in enumerate(blocks[-3][0])
                )

            if spans[1].get((row_idx, col_idx)):
                points.pop()
            points.append(p)

        for i in (-3, -1):
            b = list(blocks[i][0])
            for j, c in enumerate(b):
                if j not in points:
                    continue
                if j and b[j - 1] == "-" \
                or j < len(b) - 1 and b[j + 1] == "-":
                    b[j] = "+"
                else:
                    b[j] = "|"
            blocks[i][0] = "".join(b)

    out = []
    row_idx = 0
    for block in (blocks):
        for line in block:
            if type(line) == str:
                out.append(line)
            else:
                out.append("")
                for col_idx, col in enumerate(line):
                    sep = " " if spans[1].get((row_idx, col_idx)) else "|"
                    out[-1] += f"{sep} {col} "
                out[-1] += "|"
                row_idx += 1
    out = end.join(out)

    return out
