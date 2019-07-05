from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.ignore import IgnoredNode


class AccessNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(IgnoredNode(pos))

    @property
    def next(self):
        return self[1]

    @next.setter
    def next(self, value):
        self[1] = value
