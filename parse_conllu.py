import sys
import re

class Tree():

    def __init__(self, num_tokens):
        self.root = None
        self.node = [Node() for _ in range(num_tokens)]

    def parse(self, node):
        for child in node.child:
            self.parse(child)
            node.span.extend(child.span)
        node.span = sorted(node.span)[::len(node.span) - 1]
        node.text = " ".join(self.node[i].word for i in range(*node.span))

    def _print(self, node, depth, ls):
        ls.append((depth, node, False))
        if not node.child:
            return
        for child in sorted((node, *node.child), key = lambda x: x.idx):
            if node == child:
                ls.append((depth + 1, node, True))
                continue
            self._print(child, depth + 1, ls)

    def print_line(self):
        ls = list()
        self._print(self.root, 0, ls)
        out = list()
        prev = 0
        for depth, node, is_head in ls:
            if prev and prev >= depth:
                out.extend([")"] * (prev - depth + 1))
            pos = node.pos + ("*" if is_head else "")
            txt = " " + node.word if is_head or not node.child else ""
            out.append("%s(%s" % (pos, txt))
            prev = depth
        out.extend([")"] * (depth + 1))
        print(" ".join(out))

    def print_tree(self):
        ls = list()
        self._print(self.root, 0, ls)
        for depth, node, is_head in ls:
            pos = node.pos + ("*" if is_head else "")
            txt = node.word if is_head else node.text
            print("%s%s( %s )" % ("  " * depth, pos, txt))

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

    def __repr__(self):
        txt = "[%d] %s %s %s" % (self.idx, self.word, self.pos, self.rel)
        txt += " [%s]" % (self.head.idx if self.head else None)
        txt += " -> %s" % sorted([e.idx for e in self.child])
        return txt

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
    tree.parse(tree.root)

    return sent_id, text, tree

if __name__ == "__main__":

    block = list()

    for ln, line in enumerate(sys.stdin, 1):
        line = line.strip()

        if line == "":

            sent_id, text, tree = parse_conllu(block)

            print("sent_id =", sent_id)
            print("text =", text)
            print()

            for node in tree.node:
                print(node)
            print()

            tree.print_line()
            print()

            tree.print_tree()
            print()

            block.clear()
            continue

        block.append(line)
