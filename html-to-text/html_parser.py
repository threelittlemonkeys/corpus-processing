import re
import json
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
        self.children = []

    def __repr__(self):

        return self.tag + json.dumps({
            "span": self.span,
            "attr": self.attr,
            "text": self.text
        }, ensure_ascii = False)

def parse_html(html):

    tree = html_node()
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
            ptr.children.append(_node)

        # post-processing

        pos = node.span[1]

        if tag[:2] != "</": # opening tag

            ptr.children.append(node)

            if tag[-2:] != "/>":
                ptr = node

        else: # closing tag

            assert ptr.tag == node.tag
            ptr = ptr.parent

    return tree

def print_tree(node, pos = 0, indent = 4):

    print(" " * pos, node, sep = "")

    for child in node.children:
        print_tree(child, pos = pos + indent)

def html_to_text(html):

    tree = parse_html(html)
    print_tree(tree)
