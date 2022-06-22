import sys
import re
import random

class Tree():

    def __init__(self, num_tokens):
        self.root = None
        self.tree = list()
        self.nodes = [Node() for _ in range(num_tokens)]

    def parse_node(self, node, depth):
        node.depth = depth
        for e in node.children:
            self.parse_node(e, depth + 1)
            node.span.extend(e.span)
        node.span = sorted(node.span)[::len(node.span) - 1]
        node.text = " ".join(self.nodes[i].word for i in range(*node.span))

    def parse_tree(self, node):

        if not node.children:
            node.subtree = node.word
            return [[node.depth, node.pos, node]]

        ls = [[node.depth, node.pos, node]]
        subtree = list()
        for e in sorted((node, *node.children), key = lambda x: x.idx):
            if e == node:
                pos = node.pos + "*"
                ls.append([node.depth + 1, pos, node])
                subtree.append("%s( %s )" % (pos, node.word))
                continue
            ls.extend(self.parse_tree(e))
            subtree.append("%s( %s )" % (e.pos, e.subtree))
        node.subtree = " ".join(subtree)

        return ls

    def parse(self):
        self.parse_node(self.root, 0)
        self.tree = self.parse_tree(self.root)

    def print_tree(self):
        for depth, pos, node in self.tree:
            idx = node.span[0] if node.children and pos[-1] != "*" else node.idx
            text = node.text if node.children and pos[-1] != "*" else node.word
            print("%-4d%s%s( %s )" % (idx, "  " * depth, pos, text))

    def np_chunk(self):
        cands = dict()

        # select NP candidates
        prev = -1
        for depth, pos, node in self.tree:
            if 0 <= prev < depth:
                continue
            subtree = node.subtree if node.children and pos[-1] != "*" else node.word
            if not re.match("(ADJ|DET|NUM|NOUN|PRON|PROPN)", pos) \
            or re.search("(ADP|AUX|VERB)\*?\(", subtree):
                prev = -1
                continue
            span = [node.idx, node.idx + 1] if pos[-1] == "*" else node.span
            cands[node.idx] = [node, span, True]
            prev = depth

        # merge NP fragments
        for idx, cand in cands.items():
            if not re.match("(DET|NUM|NOUN|PRON|PROPN)", cand[0].pos):
                cand[2] = False
            children = [e.idx for e in cand[0].children if e.idx in cands]
            for i in sorted(children, key = lambda x: abs(x - idx)):
                for j in range(2):
                    if cand[1][j] == cands[i][1][1 - j]:
                        cand[1][j] = cands[i][1][j]
                        cands[i][2] = False
                        break
        cands = [cands[e][1] for e in cands if cands[e][2]]

        # multi-word tokens
        ks = list()
        sent = list()
        for i, node in enumerate(self.nodes):
            word = node.word.split(" ")
            sent.extend(word)
            ks.append((ks[-1] if ks else 0) + len(word) - 1)
        cands = [[i + ks[i] if i else 0, j + ks[j - 1]] for i, j in cands]

        # IOB tagging
        words = [word for word in sent]
        tags = ["O"] * len(sent)
        for span in cands:
            for i in range(*span):
                if re.search("[0-9A-Za-z\u0400-\u04FF]", sent[i]):
                    break
            for j in range(*span[::-1], -1):
                if re.search("[0-9A-Za-z\u0400-\u04FF]", sent[j - 1]):
                    break
            sent[i] = "NP( " + sent[i]
            sent[j - 1] += " )"
            tags[i:j] = ["B-NP"] + ["I-NP"] * (j - i - 1)

        return " ".join(sent), words, tags

class Node():

    def __init__(self):
        self.idx = None
        self.word = None
        self.pos = None
        self.rel = None
        self.span = None
        self.text = None
        self.head = None
        self.children = set()
        self.depth = None
        self.subtree = None

    def __repr__(self):
        text = "[%d] %s %s %s" % (self.idx, self.word, self.pos, self.rel)
        text += " [%s]" % (self.head.idx if self.head else None)
        text += " -> %s" % sorted([e.idx for e in self.children])
        return text

def postprocess(tree):

    for node in tree.nodes:

        if node.pos == "ADP" and node.head.pos == "NOUN":
            child = node.head
            head = child.head
            node.head = head
            node.children.add(child)
            head.children |= {node}
            head.children -= {child}
            child.head = node
            child.children -= {node}

            for e in list(child.children):
                if e.idx < node.idx < child.idx:
                    e.head = node
                    node.children |= {e}
                    child.children -= {e}

def parse_conllu(block):

    try:
        sent_id = next(filter(lambda x: re.match("# sent_id = ", x), block))
        sent_id = re.sub("^# sent_id = ", "", sent_id)
        text = next(filter(lambda x: re.match("# text = ", x), block))
        text = re.sub("^# text = ", "", text)
    except:
        sent_id = None
        text = None

    rows = [row.strip().split("\t") for row in block if row.count("\t") == 9]
    tree = Tree(len(rows))

    for idx, (row, node) in enumerate(zip(rows, tree.nodes)):

        _, form, lemma, upos, xpos, feats, head, deprel, deps, misc = row

        node.idx = idx
        node.word = form
        node.pos = upos
        node.rel = deprel
        node.span = [idx, idx + 1]

        head = int(head) - 1
        if head == -1:
            tree.root = node
            continue

        node.head = tree.nodes[head]
        node.head.children.add(node)

    postprocess(tree)
    tree.parse()

    return sent_id, text, tree

if __name__ == "__main__":

    block = list()
    results = list()

    for ln, line in enumerate(sys.stdin, 1):
        line = line.strip()

        if line != "":
            block.append(line)
            continue

        try:
            result = parse_conllu(block)
            results.append(result)
        except:
            pass

        block.clear()

    # random.shuffle(results)
    for idx, result in enumerate(results, 1):
        sent_id, text, tree = result

        print("# sent_id =", sent_id)
        print("# text =", text)
        print()

        for node in tree.nodes:
            print(node)
        print()

        tree.print_tree()
        print()

        sent, words, tags = tree.np_chunk()
        print(sent)
        print(" ".join(["%s/%s" % x for x in zip(words, tags)]))
        print()
