class Node:
    def __init__(self, pos, children=None):
        if children is None:
            children = []
        self.children = children
        self.pos = pos
        self.parent = None
        for child in self.children:
            if isinstance(child, Node):
                child.parent = self

    def __len__(self):
        return len(self.children)

    def __getitem__(self, key):
        return self.children[key]

    def __setitem__(self, key, value):
        if isinstance(value, Node):
            value.parent = self
        self.children[key] = value

    def append(self, node):
        if isinstance(node, Node):
            node.parent = self
        self.children.append(node)

    def pop(self, index):
        return self.children.pop(index)

    def print(self):
        self._print(first=True)

    def _print(self, prefix="", last=True, first=False):
        print(prefix, '' if first else '└─' if last else '├─', self.__class__.__name__, f" (line {self.pos[0]+1}, col {self.pos[1]+1})", sep="")
        prefix += '   ' if last else '│  '
        for i, child in enumerate(self.children):
            last = i == len(self.children) - 1
            if isinstance(child, Node):
                child._print(prefix, last)
            else:
                print(prefix, '└' if last else '├', f"'{str(child)}'", sep="")

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def withChildren(cls, children, pos):
        node = cls(pos)
        node.children = children
        return node


class ParseResult():
    def __init__(self, result, node):
        if result and node is None:
            raise RuntimeError("Node musn't be None if result is set to True for ParseResult")
        self.result = result
        self.node = node

    @staticmethod
    def FAIL():
        return ParseResult(False, None)

    @staticmethod
    def OK(node):
        return ParseResult(True, node)

    def __str__(self):
        return f"{'OK' if self.result else 'FAILED'}[{self.node}]"


