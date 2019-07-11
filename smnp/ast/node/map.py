from smnp.ast.node.atom import LiteralParser
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.operator import BinaryOperator, Operator
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class MapEntry(BinaryOperator):

    @property
    def key(self):
        return self[0]

    @key.setter
    def key(self, value):
        self[0] = value

    @property
    def value(self):
        return self[2]

    @value.setter
    def value(self, value):
        self[2] = value


class Map(Node):
    pass


def MapParser(input):
    from smnp.ast.node.expression import ExpressionParser
    keyParser = LiteralParser
    valueParser = ExpressionParser

    mapEntryParser = Parser.allOf(
        keyParser,
        Parser.terminalParser(TokenType.ARROW, createNode=Operator.withValue),
        valueParser,
        createNode=MapEntry.withValues
    )

    mapParser = abstractIterableParser(Map, TokenType.OPEN_CURLY, TokenType.CLOSE_CURLY, mapEntryParser)

    return Parser(mapParser, "map", [mapParser])(input)
