from smnp.ast.node.atom import Atom
from smnp.ast.node.expression import ExpressionParser
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.operator import BinaryOperator, Operator
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Identifier(Atom):
    pass


class FunctionCall(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode()]

    @property
    def name(self):
        return self[0]

    @name.setter
    def name(self, value):
        self[0] = value

    @property
    def arguments(self):
        return self[1]

    @arguments.setter
    def arguments(self, value):
        self[1] = value

    @classmethod
    def withChildren(cls, name, arguments):
        node = cls(name.pos)
        node.name = name
        node.arguments = arguments
        return node


class ArgumentsList(Node):
    pass


class Assignment(BinaryOperator):
    pass


def IdentifierLiteralParser(input):
    return Parser.terminal(TokenType.IDENTIFIER, createNode=Identifier.withValue)(input)


def IdentifierParser(input):


    functionCallParser = Parser.allOf(
        IdentifierLiteralParser,
        abstractIterableParser(ArgumentsList, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, ExpressionParser),
        createNode=lambda name, arguments: FunctionCall.withChildren(name, arguments)
    )

    assignmentParser = Parser.allOf(
        IdentifierLiteralParser,
        Parser.terminal(TokenType.ASSIGN, createNode=Operator.withValue),
        ExpressionParser,
        createNode=lambda identifier, assign, expr: Assignment.withValues(identifier, assign, expr)
    )

    return Parser.oneOf(
        assignmentParser,
        functionCallParser,
        IdentifierLiteralParser
    )(input)
