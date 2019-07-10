from smnp.ast.node.access import LeftAssociativeOperatorNode
from smnp.ast.node.bool import BoolLiteralNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.none import NoneNode
from smnp.ast.node.note import NoteLiteralNode
from smnp.ast.node.string import StringLiteralNode
from smnp.ast.node.type import TypeNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType

class MapEntry(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode()]

    @property
    def key(self):
        return self[0]

    @key.setter
    def key(self, value):
        self[0] = value

    @property
    def value(self):
        return self[1]

    @value.setter
    def value(self, value):
        self[1] = value

class MapNode(LeftAssociativeOperatorNode):

    @classmethod
    def _literalParser(cls):
        return abstractIterableParser(MapNode, TokenType.OPEN_CURLY, TokenType.CLOSE_CURLY, cls._entryParser())

    @classmethod
    def _entryParser(cls):
        def createNode(key, arrow, value):
            node = MapEntry(key.pos)
            node.key = key
            node.value = value
            return node

        return Parser.allOf(
            cls._keyParser(),
            Parser.terminalParser(TokenType.ARROW),
            ExpressionNode.parse,
            createNode=createNode
        )

    @classmethod
    def _keyParser(cls):
        return Parser.oneOf(
            IntegerLiteralNode._literalParser(),
            StringLiteralNode._literalParser(),
            NoteLiteralNode._literalParser(),
            BoolLiteralNode._literalParser(),
            TypeNode.parse
        )