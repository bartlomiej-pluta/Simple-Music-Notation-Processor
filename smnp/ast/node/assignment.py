from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.none import NoneNode


class AssignmentNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(NoneNode())

    @property
    def target(self):
        return self[0]

    @target.setter
    def target(self, value):
        self[0] = value

    @property
    def value(self):
        return self[1]

    @value.setter
    def value(self, value):
        self[1] = value

    @classmethod
    def _parse(cls, input):
        raise RuntimeError("This class is not supposed to be automatically called")