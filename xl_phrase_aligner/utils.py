import numpy as np

def cos_similarity(x, y):
    z = np.linalg.norm(x) * np.linalg.norm(y)
    return np.dot(x, y) / (z if z else 1)

def phrase_iter(tokens, phrase_maxlen):
    for i in range(len(tokens)):
        for j in range(i + 1, min(len(tokens), i + phrase_maxlen) + 1):
            phrase = tokens[i:j]
            if validate_phrase(phrase):
                yield (i, j), " ".join(phrase)

def validate_phrase(phrase):
    if len(phrase) > 1 and phrase[-1] in (",", ".", "?", "!", "the"):
        return False
    return True
