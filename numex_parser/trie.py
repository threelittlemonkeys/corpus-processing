class trie_node():

    def __init__(self):
        self.key = ""
        self.value = None
        self.children = {}
        self.prefix = None # (node, pos)

class trie():

    def __init__(self):
        self.root = trie_node()
        self.optimized = False
        self.ignore_case = False
        self.ignore_space = False
        self.verbose = True

    def __repr__(self):
        if not self.optimized:
            self.optimize()
        out = []
        def _print(node, depth):
            indent = "  " * depth
            prefix = f" -> {node.prefix[1]}" if node.prefix else ""
            out.append(f"{indent}[{node.key}] {node.value}{prefix}")
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
            if c == " " and self.ignore_space:
                continue
            if c not in node.children:
                node.children[c] = trie_node()
                node.children[c].key = c
            node = node.children[c]
        node.value = value
        self.optimized = False

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
        self.optimized = True

    def find(self, key):
        node = self.root
        for c in key:
            if c not in node.children:
                return None
            node = node.children[c]
        return node

    def search(self, txt):
        if not self.optimized:
            self.optimize()
        i, j = 0, 0
        node = self.root
        _txt = txt + "$"
        if self.ignore_space:
            _pos = [i for i, c in enumerate(_txt) if c != " "]
            _txt = _txt.replace(" ", "")
        matches = []
        out = []
        while j < len(_txt):
            c = _txt[j]
            out += [("span =", (i, j, _txt[i:j]))]
            if c in node.children: # if child exists
                j += 1
                node = node.children[c]
            elif node.value != None: # if value exists
                matches.append((i, j, _txt[i:j], node.value))
                i = j
                node = self.root
                out += [("matches =", matches)]
            elif node.prefix: # if prefix exists
                i = j + node.prefix[1]
                node = node.prefix[0]
                out += [("prefix =", (i, j, _txt[i:j]))]
            else:
                j += 1
                i = j
                node = self.root
        if self.ignore_space:
            matches = [
                (_pos[i], _pos[j], txt[_pos[i]:_pos[j]], value)
                for i, j, _, value in matches
            ]
        if self.verbose:
            for line in out:
                print(*line)
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

    print(trie)
    print(trie.search("shis"))
