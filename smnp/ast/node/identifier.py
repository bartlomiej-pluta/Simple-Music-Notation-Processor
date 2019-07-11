from smnp.ast.node.atom import Atom
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.operator import BinaryOperator, Operator
from smnp.ast.parser import Parsers
from smnp.token.type import TokenType
from smnp.util.singleton import SingletonParser


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


@SingletonParser
def IdentifierParser():
    identifierLiteralParser = Parsers.terminal(TokenType.IDENTIFIER, createNode=Identifier.withValue)

    functionCallParser = Parsers.allOf(
        identifierLiteralParser,
        #abstractIterableParser(ArgumentsList, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, MaxPrecedenceExpressionParser),
        createNode=lambda name, arguments: FunctionCall.withChildren(name, arguments),
        name="functionCall"
    )

    assignmentParser = Parsers.allOf(
        identifierLiteralParser,
        Parsers.terminal(TokenType.ASSIGN, createNode=Operator.withValue),
        #MaxPrecedenceExpressionParser,
        createNode=lambda identifier, assign, expr: Assignment.withValues(identifier, assign, expr),
        name="assignment"
    )

    return Parsers.oneOf(
        assignmentParser,
        functionCallParser,
        identifierLiteralParser,
        name="idExpr"
    )
