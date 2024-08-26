import numpy as np

def cos_similarity(x, y):

    z = np.linalg.norm(x) * np.linalg.norm(y)

    return np.dot(x, y) / (z if z else 1)

def batch_iter(filename, batch_size):

    batch = []

    with open(filename) as fo:
        while True:
            line = fo.readline()
            if line:
                batch.append(line.strip())
                if len(batch) < batch_size:
                    continue
            if batch:
                yield batch
                batch.clear()
            if not line:
                break

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
