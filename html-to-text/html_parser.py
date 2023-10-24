import re
import json
from table_parser import *
from utils import *

_PT_TAG = r"</?([^!'\"> ]+)((?:[^'\"/>]+|'(?:[^']|\\')*'|\"(?:[^\"]|\\\")*\")*)/?>"
_PT_ATTR = r"([^'\"= ]+) *= *([^'\" ]+|'(?:[^']|\\')*'|\"(?:[^\"]|\\\")*\")"

class html_node():

    def __init__(self):

        self.tag = ""
        self.span = [0, 0]
        self.attr = {}
        self.text = ""
        self.parent = None
        self.sibling = None
        self.children = []

    def __repr__(self):

        return self.tag + json.dumps({
            "span": self.span,
            "attr": self.attr,
            "text": self.text
        }, ensure_ascii = False)

    def nextup(self, node = None):

        if not node:
            node = self

        if node.sibling:
            return node.sibling

        return self.nextup(node.parent)

    def nextdown(self, node = None):

        if not node:
            node = self

        if node.children:
            return node.children[0]

        while node:
            if node.sibling:
                return node.sibling
            node = node.parent

        return node

    def iter(self, node = None, depth = 0):

        if not node:
            node = self

        yield (node, depth)

        for child in node.children:
            yield from self.iter(child, depth + 1)

    def print(self, indent = 4):

        for node, depth in self.iter():
            print(" " * (depth * indent), node, sep = "")

def parse_html(html):

    tree = html_node()
    tree.tag = "root"
    pos = 0
    ptr = tree

    for m in re.finditer(_PT_TAG, html):

        node = html_node()

        # tag node

        tag = m.group()
        node.tag, node.attr = m.groups()
        node.span = [*m.span()]
        node.attr = {
            m.group(1): re.sub("^['\"]|['\"]$", "", m.group(2))
            for m in re.finditer(_PT_ATTR, node.attr)
        }
        node.parent = ptr

        # text node

        if pos != node.span[0]:

            _node = html_node()
            _node.span = [pos, node.span[0]]
            _node.text = normalize_html(html[pos:node.span[0]])
            _node.parent = ptr

            if ptr.children:
                ptr.children[-1].sibling = _node
            ptr.children.append(_node)

        # post-processing

        pos = node.span[1]

        if tag[:2] != "</": # opening tag

            if ptr.children:
                ptr.children[-1].sibling = node
            ptr.children.append(node)

            if tag[-2:] != "/>":
                ptr = node

        else: # closing tag

            assert ptr.tag == node.tag
            ptr.span[1] = pos
            ptr = ptr.parent

    return tree

def html_to_text(html):

    node = parse_html(html)

    while node:

        if node.tag == "table":

            print("--->", node)
            node = node.nextup()

        else:

            print(node)
            node = node.nextdown()
