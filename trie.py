class trie_node():

    def __init__(self):
        self.key = ""
        self.value = None
        self.children = {}
        self.prefix = None # (node, pos)

class trie():

    def __init__(self):
        self.root = trie_node()

    def __repr__(self):
        out = []
        def _print(node, depth):
            ind = "  " * depth # indent
            out.append("%s[%s] %s" % (ind, node.key, node.value))
            for child in node.children.values():
                _print(child, depth + 1)
        _print(self.root, 0)
        return "\n".join(out)

    def __getitem__(self, key):
        if self.find(key):
            return self.find(key).value
        return None

    def __setitem__(self, key, value):
        node = self.root
        for c in key:
            if c == " ":
                continue
            if c not in node.children:
                node.children[c] = trie_node()
                node.children[c].key = c
            node = node.children[c]
        node.value = value

    def find(self, key):
        node = self.root
        for c in key:
            if c not in node.children:
                return None
            node = node.children[c]
        return node

    def optimize(self):
        def _optimize(node, prefix):
            prefix += node.key
            for i in range(1, len(prefix)):
                _node = self.find(prefix[i:])
                if _node: # longest prefix
                    node.prefix = (_node, i - len(prefix))
                    break
            for child in node.children.values():
                _optimize(child, prefix)
        _optimize(self.root, "")

    def search(self, txt):
        i, j = 0, 0
        node = self.root
        _txt = [*txt, None]
        matches = []
        while j < len(_txt):
            c = _txt[j]
            if c in node.children: # if child exists
                j += 1
                node = node.children[c]
            elif node.value != None: # if value exists
                matches.append((i, j, txt[i:j], node.value))
                i = j
                node = self.root
            elif c == " ":
                if i == j:
                    i += 1
                j += 1
            elif node.prefix: # if prefix exists
                i = j + node.prefix[1]
                node = node.prefix[0]
            else:
                j += 1
                i = j
                node = self.root
        return matches

    def replace(self, txt, func):
        d = 0
        matches = self.search(txt)
        for i, j, key, value in matches:
            out = func(key, value)
            txt = txt[:i + d] + out + txt[j + d:]
            d = len(out) - len(key)
        return txt

if __name__ == "__main__":

    trie = trie()

    trie["he"] = 0
    trie["her"] = 1
    trie["his"] = 2
    trie["is"] = 3
    trie["she"] = 4

    trie.optimize()

    print(trie)
    print(trie.search("shis"))
