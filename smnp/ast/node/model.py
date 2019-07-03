from smnp.note.model import Note

class Node:
    def __init__(self, parent, pos):
        self.children = []
        self.parent = parent
        self.pos = pos
        for child in self.children:
            child.parent = self

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def append(self, node):
        node.parent = self
        self.children.append(node)

    def pop(self, index):
        return self.children.pop(index)

    def _print(self, level):
        string = f"{pad(level)}{self.__class__.__name__}({self.parent.__class__.__name__}):\n"
        for child in self.children:
            if isinstance(child, str) or isinstance(child, int) or isinstance(child, Note):
                string += pad(level + 1) + f"'{child}'\n"
            else:
                string += child._print(level + 1)
        return string

    def __str__(self):
        return self._print(0)


def pad(level):
    return ("   " * level)