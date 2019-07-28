from smnp.ast.node.model import Node
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Atom(Node):
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


class IntegerLiteral(Atom):
    pass


class FloatLiteral(Atom):
    pass


class StringLiteral(Atom):
    pass


class NoteLiteral(Atom):
    pass


class BoolLiteral(Atom):
    pass


class TypeLiteral(Atom):
    pass


def IntegerParser(input):
    return Parser.terminal(TokenType.INTEGER, createNode=IntegerLiteral.withValue)(input)


def FloatParser(input):
    return Parser.terminal(TokenType.FLOAT, createNode=FloatLiteral.withValue)(input)


def StringParser(input):
    return Parser.terminal(TokenType.STRING, createNode=StringLiteral.withValue)(input)


def NoteParser(input):
    return Parser.terminal(TokenType.NOTE, createNode=NoteLiteral.withValue)(input)


def BoolParser(input):
    return Parser.terminal(TokenType.BOOL, createNode=BoolLiteral.withValue)(input)


def TypeLiteralParser(input):
    return Parser.terminal(TokenType.TYPE, createNode=TypeLiteral.withValue)(input)


def LiteralParser(input):
    return Parser.oneOf(
        IntegerParser,
        FloatParser,
        StringParser,
        NoteParser,
        BoolParser,
        TypeLiteralParser,
        name="literal"
    )(input)


def AtomParser(input):
    from smnp.ast.node.identifier import IdentifierParser
    from smnp.ast.node.list import ListParser
    from smnp.ast.node.map import MapParser
    from smnp.ast.node.expression import ExpressionParser

    parentheses = Parser.allOf(
        Parser.terminal(TokenType.OPEN_PAREN),
        Parser.doAssert(ExpressionParser, "expression"),
        Parser.terminal(TokenType.CLOSE_PAREN),
        createNode=lambda open, expr, close: expr,
        name="grouping parentheses"
    )

    return Parser.oneOf(
        parentheses,
        LiteralParser,
        IdentifierParser,
        ListParser,
        MapParser,
        name="atom"
    )(input)


