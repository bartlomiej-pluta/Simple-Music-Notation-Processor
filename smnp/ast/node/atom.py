from smnp.ast.node.model import Node
from smnp.ast.parser import Parsers
from smnp.token.type import TokenType
from smnp.util.singleton import SingletonParser


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


@SingletonParser
def IntegerParser():
    return Parsers.oneOf(
        Parsers.terminal(TokenType.INTEGER, lambda val, pos: IntegerLiteral.withValue(int(val), pos)),
        Parsers.allOf(
            Parsers.terminal(TokenType.MINUS),
            Parsers.terminal(TokenType.INTEGER, lambda val, pos: IntegerLiteral.withValue(int(val), pos)),
            createNode=lambda minus, integer: IntegerLiteral.withValue(-integer.value, minus.pos),
            name="negativeInteger"
        ),
        name="int"
    )


@SingletonParser
def StringParser():
    return Parsers.terminal(TokenType.STRING, createNode=StringLiteral.withValue)


@SingletonParser
def NoteParser():
    return Parsers.terminal(TokenType.NOTE, createNode=NoteLiteral.withValue)


@SingletonParser
def BoolParser():
    return Parsers.terminal(TokenType.BOOL, createNode=BoolLiteral.withValue)


@SingletonParser
def TypeParser():
    return Parsers.terminal(TokenType.TYPE, createNode=TypeLiteral.withValue)


@SingletonParser
def LiteralParser():
    return Parsers.oneOf(
        IntegerParser(),
        StringParser(),
        NoteParser(),
        BoolParser(),
        TypeParser(),
        name="literal"
    )


@SingletonParser
def AtomParser():
    from smnp.ast.node.identifier import IdentifierParser

    return Parsers.oneOf(
        LiteralParser(),
        IdentifierParser(),
        name="atom"
    )


