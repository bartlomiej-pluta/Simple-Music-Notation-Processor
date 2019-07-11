from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode


class UnaryOperator(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children=[NoneNode(), NoneNode()]

    @property
    def operator(self):
        return self[0]

    @operator.setter
    def operator(self, value):
        self[0] = value

    @property
    def value(self):
        return self[1]

    @value.setter
    def value(self, value):
        self[1] = value

    @classmethod
    def withValues(cls, operator, value):
        node = cls(operator.pos)
        node.operator = operator
        node.value = value
        return node


class BinaryOperator(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

    @property
    def left(self):
        return self[0]

    @left.setter
    def left(self, value):
        self[0] = value

    @property
    def operator(self):
        return self[1]

    @operator.setter
    def operator(self, value):
        self[1] = value

    @property
    def right(self):
        return self[2]

    @right.setter
    def right(self, value):
        self[2] = value

    @classmethod
    def withValues(cls, left, operator, right):
        node = cls(operator.pos)
        node.left = left
        node.operator = operator
        node.right = right
        return node


class Operator(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @property
    def value(self):
        return self[0]

    @value.setter
    def value(self, value):
        self[0] = value

    @classmethod
    def withValue(cls, value, pos):
        node = cls(pos)
        node.value = value
        return node