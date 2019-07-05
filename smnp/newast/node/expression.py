from smnp.newast.node.asterisk import AsteriskNode
from smnp.newast.node.model import Node
from smnp.newast.node.none import NoneNode
from smnp.newast.node.statement import StatementNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


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
    def withValue(cls, val, pos):
        node = cls(pos)
        node.value = val
        return node

    @classmethod
    def _parse(cls, input):
        return Parser.oneOf(
            cls._asteriskParser(),
            cls._expressionParser(),
        )(input)

    @classmethod
    def _asteriskParser(cls):
        def createNode(iterator, asterisk, statement):
            node = AsteriskNode(asterisk.pos)
            node.iterator = iterator
            node.statement = statement
            return node

        return Parser.allOf(
            cls._expressionParser(),
            Parser.terminalParser(TokenType.ASTERISK),
            StatementNode.parse,
            createNode=createNode
        )

    @classmethod
    def _expressionParser(cls):
        from smnp.newast.node.integer import IntegerLiteralNode
        from smnp.newast.node.string import StringLiteralNode
        from smnp.newast.node.note import NoteLiteralNode
        from smnp.newast.node.identifier import IdentifierNode
        from smnp.newast.node.list import ListNode

        return Parser.oneOf(
            IntegerLiteralNode.parse,
            StringLiteralNode.parse,
            NoteLiteralNode.parse,
            IdentifierNode.parse,
            ListNode.parse
        )