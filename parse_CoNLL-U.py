import sys
import re

class Tree():

    def __init__(self, num_tokens):
        self.root = None
        self.node = [Node() for _ in range(num_tokens)]
        self.tree = list()

    def parse_node(self, node, depth):
        node.depth = depth
        for e in node.child:
            self.parse_node(e, depth + 1)
            node.span.extend(e.span)
        node.span = sorted(node.span)[::len(node.span) - 1]
        node.text = " ".join(self.node[i].word for i in range(*node.span))

    def parse_tree(self, node):

        if not node.child:
            node.subtree = node.word
            return [[node.depth, node.pos, node]]

        ls = [[node.depth, node.pos, node]]
        subtree = list()
        for e in sorted((node, *node.child), key = lambda x: x.idx):
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
            text = node.text if node.child and pos[-1] != "*" else node.word
            print("%s%s( %s )" % ("  " * depth, pos, text))

    def np_chunk(self):
        ls = list()
        prev = -1
        for depth, pos, node in self.tree:
            if 0 <= prev < depth:
                continue

            subtree = node.subtree if node.child and pos[-1] != "*" else node.word
            if not re.match("(ADJ|NOUN)", pos) \
            or re.search("ADP\*\(", subtree):
                prev = -1
                continue

            span = [node.idx, node.idx + 1] if pos[-1] == "*" else node.span
            if ls and span[0] == ls[-1][1] and (
            node.head and ls[-1][0] <= node.head.idx < ls[-1][1]
            or any(ls[-1][0] <= e.idx < ls[-1][1] for e in node.child)):
                ls[-1][1] = span[1]
            else:
                ls.append(span)
            prev = depth

        text = [node.word for node in self.node]
        words = [node.word for node in self.node]
        tags = ["O"] * len(self.node)

        for k, span in enumerate(ls):
            for i in range(*span):
                if re.search("[0-9A-Za-z\u0400-\u04FF]", self.node[i].word):
                    break
            for j in range(*span[::-1], -1):
                if re.search("[0-9A-Za-z\u0400-\u04FF]", self.node[j - 1].word):
                    break
            text[i] = "NP( " + text[i]
            text[j - 1] += " )"
            tags[i:j] = ["B"] + ["I"] * (j - i - 1)

        return " ".join(text), words, tags

class Node():

    def __init__(self):
        self.idx = None
        self.word = None
        self.pos = None
        self.rel = None
        self.span = None
        self.text = None
        self.head = None
        self.child = set()
        self.depth = None
        self.subtree = None

    def __repr__(self):
        text = "[%d] %s %s %s" % (self.idx, self.word, self.pos, self.rel)
        text += " [%s]" % (self.head.idx if self.head else None)
        text += " -> %s" % sorted([e.idx for e in self.child])
        return text

def postprocess(tree):

    for node in tree.node:

        if node.pos == "ADP" and node.head.pos == "NOUN":
            child = node.head
            head = child.head
            node.head = head
            node.child.add(child)
            head.child |= {node}
            head.child -= {child}
            child.head = node
            child.child -= {node}

            for e in list(child.child):
                if e.head == child and e.idx < node.idx < child.idx:
                    e.head = node
                    node.child |= {e}
                    child.child -= {e}

def parse_conllu(block):

    try:
        sent_id = next(filter(lambda x: re.match("# sent_id = ", x), block))
        sent_id = re.sub("^# sent_id = ", "", sent_id)
        text = next(filter(lambda x: re.match("# text = ", x), block))
        text = re.sub("^# text = ", "", text)
    except:
        sent_id = None
        text = None

    tokens = [row.strip().split("\t") for row in block if row.count("\t") == 9]
    tree = Tree(len(tokens))

    for idx, (cols, node) in enumerate(zip(tokens, tree.node)):

        _, form, lemma, upos, xpos, feats, head, deprel, deps, misc = cols

        node.idx = idx
        node.word = form
        node.pos = upos
        node.rel = deprel
        node.span = [idx, idx + 1]

        head = int(head) - 1
        if head == -1:
            tree.root = node
            continue

        node.head = tree.node[head]
        node.head.child.add(node)

    postprocess(tree)
    tree.parse()

    return sent_id, text, tree

if __name__ == "__main__":

    block = list()

    for ln, line in enumerate(sys.stdin, 1):

        line = line.strip()

        if line != "":
            block.append(line)
            continue

        try:
            result = parse_conllu(block)
        except:
            result = None

        if result:
            sent_id, text, tree = result

            print("sent_id =", sent_id)
            print("text =", text)
            print()

            for node in tree.node:
                print(node)
            print()

            tree.print_tree()
            print()

            text, words, tags = tree.np_chunk()
            print(text)
            print(words)
            print(tags)
            print()

        block.clear()
