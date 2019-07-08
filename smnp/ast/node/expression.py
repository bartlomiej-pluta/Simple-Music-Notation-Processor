from smnp.ast.node.asterisk import AsteriskNode
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.statement import StatementNode
from smnp.ast.parser import Parser
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
            Parser.doAssert(StatementNode.parse, 'statement'),
            createNode=createNode
        )

    @classmethod
    def _expressionParser(cls):
        from smnp.ast.node.integer import IntegerLiteralNode
        from smnp.ast.node.string import StringLiteralNode
        from smnp.ast.node.note import NoteLiteralNode
        from smnp.ast.node.identifier import IdentifierNode
        from smnp.ast.node.list import ListNode
        from smnp.ast.node.map import MapNode

        return Parser.oneOf(
            IntegerLiteralNode.parse,
            StringLiteralNode.parse,
            NoteLiteralNode.parse,
            IdentifierNode.parse,
            MapNode.parse,
            ListNode.parse
        )