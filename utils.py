def trim(x):
    y = ""
    for c in x:
        if c <= "\u0020":
            if len(y) and y[-1] != " ":
                y += " "
            continue
        y += c
    if len(y) and y[-1] == " ":
        y = y[:-1]
    return y

def isnumeric(x):
    if not x:
        return False
    for c in x:
        if not "0" <= c <= "9":
            return False
    return True

def isalpha(x):
    if not x:
        return False
    for c in x:
        if not ("A" <= c <= "Z" or "a" <= c <= "z"):
            return False
    return True
