from smnp.newast.node.model import Node
from smnp.newast.node.none import NoneNode
from smnp.newast.parser import Parser


class ExpressionNode(Node):
    def __init__(self, pos):
        super().__init__(pos, [NoneNode()])

    @property
    def value(self):
        return self[0]


    @value.setter
    def value(self, v):
        self[0] = v


    @classmethod
    def withValue(cls, pos, v):
        node = cls(pos)
        node.value = v
        return node


    @classmethod
    def _parse(cls, input):
        from smnp.newast.node.integer import IntegerLiteralNode
        from smnp.newast.node.string import StringLiteralNode
        from smnp.newast.node.list import ListNode

        return Parser.oneOf(
            IntegerLiteralNode.parse,
            StringLiteralNode.parse,
            ListNode.parse
        )(input)