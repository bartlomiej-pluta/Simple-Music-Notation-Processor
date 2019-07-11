from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode


class IfElse(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

    @property
    def condition(self):
        return self[0]

    @condition.setter
    def condition(self, value):
        self[0] = value

    @property
    def ifNode(self):
        return self[1]

    @ifNode.setter
    def ifNode(self, value):
        self[1] = value

    @property
    def elseNode(self):
        return self[2]

    @elseNode.setter
    def elseNode(self, value):
        self[2] = value

    @classmethod
    def createNode(cls, ifNode, condition, elseNode=NoneNode()):
        node = cls(ifNode.pos)
        node.ifNode = ifNode
        node.condition = condition
        node.elseNode = elseNode
        return node


