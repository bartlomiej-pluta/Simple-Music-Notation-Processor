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


class StringLiteral(Atom):
    pass


class NoteLiteral(Atom):
    pass


class BoolLiteral(Atom):
    pass


class TypeLiteral(Atom):
    pass


def IntegerParser(input):
    return Parser.oneOf(
        Parser.terminalParser(TokenType.INTEGER, lambda val, pos: IntegerLiteral.withValue(int(val), pos)),
        Parser.allOf(
            Parser.terminalParser(TokenType.MINUS),
            Parser.terminalParser(TokenType.INTEGER, lambda val, pos: IntegerLiteral.withValue(int(val), pos)),
            createNode=lambda minus, integer: IntegerLiteral.withValue(-integer.value, minus.pos),
            name="negative integer"
        )
    )(input)


def StringParser(input):
    return Parser.terminalParser(TokenType.STRING, createNode=StringLiteral.withValue)(input)


def NoteParser(input):
    return Parser.terminalParser(TokenType.NOTE, createNode=NoteLiteral.withValue)(input)


def BoolParser(input):
    return Parser.terminalParser(TokenType.BOOL, createNode=BoolLiteral.withValue)(input)


def TypeLiteralParser(input):
    return Parser.terminalParser(TokenType.TYPE, createNode=TypeLiteral.withValue)(input)


def LiteralParser(input):
    return Parser.oneOf(
        IntegerParser,
        StringParser,
        NoteParser,
        BoolParser,
        TypeLiteralParser,
        name="literal"
    )(input)


def AtomParser(input):
    from smnp.ast.node.identifier import IdentifierParser

    return Parser.oneOf(
        LiteralParser,
        IdentifierParser,
        name="atom"
    )(input)


