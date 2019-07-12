from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode


class Valuable(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode()]

    @property
    def value(self):
        return self[0]

    @value.setter
    def value(self, value):
        self[0] = value

    @classmethod
    def withValue(cls, value, pos=None):
        node = cls(value.pos if pos is None else pos)
        node.value = value
        return node