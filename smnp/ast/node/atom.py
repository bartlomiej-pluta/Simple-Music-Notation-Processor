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

def AtomParser(input):
    from smnp.ast.node.identifier import IdentifierParser

    integerParser = Parser.oneOf(
        Parser.terminalParser(TokenType.INTEGER, lambda val, pos: IntegerLiteral.withValue(int(val), pos)),
        Parser.allOf(
            Parser.terminalParser(TokenType.MINUS),
            Parser.terminalParser(TokenType.INTEGER, lambda val, pos: IntegerLiteral.withValue(int(val), pos)),
            createNode=lambda minus, integer: IntegerLiteral.withValue(-integer.value, minus.pos)
        )
    )

    parser = Parser.oneOf(
        integerParser,
        Parser.terminalParser(TokenType.STRING, lambda val, pos: StringLiteral.withValue(val, pos)),
        Parser.terminalParser(TokenType.NOTE, lambda val, pos: NoteLiteral.withValue(val, pos)),
        Parser.terminalParser(TokenType.BOOL, lambda val, pos: BoolLiteral.withValue(val, pos)),
        IdentifierParser,
    )

    return Parser(parser, "atom", parser)(input)
