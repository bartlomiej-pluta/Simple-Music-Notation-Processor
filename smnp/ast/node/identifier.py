from smnp.ast.node.atom import Atom
from smnp.ast.node.expression import MaxPrecedenceExpressionParser
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


def IdentifierParser(input):
    identifierLiteralParser = Parser.terminalParser(TokenType.IDENTIFIER, createNode=Identifier.withValue)

    functionCallParser = Parser.allOf(
        identifierLiteralParser,
        abstractIterableParser(ArgumentsList, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, MaxPrecedenceExpressionParser),
        createNode=lambda name, arguments: FunctionCall.withChildren(name, arguments)
    )

    assignmentParser = Parser.allOf(
        identifierLiteralParser,
        Parser.terminalParser(TokenType.ASSIGN, createNode=Operator.withValue),
        MaxPrecedenceExpressionParser,
        createNode=lambda identifier, assign, expr: Assignment.withValues(identifier, assign, expr)
    )

    return Parser.oneOf(
        assignmentParser,
        functionCallParser,
        identifierLiteralParser
    )(input)


    #
    # def __init__(self, pos):
    #     super().__init__(pos)
    #     self.children = [None]
    #
    # @classmethod
    # def _lhsParser(cls):
    #     return Parser.oneOf(
    #         IdentifierNode._functionCallParser(),
    #         IdentifierNode._assignmentParser(),
    #         IdentifierNode.identifierParser()
    #     )
    #
    # @staticmethod
    # def _assignmentParser():
    #     def createNode(target, assignment, value):
    #         node = AssignmentNode(assignment.pos)
    #         node.target = target
    #         node.value = value
    #         return node
    #
    #     return Parser.allOf(
    #         IdentifierNode.identifierParser(),
    #         Parser.terminalParser(TokenType.ASSIGN),
    #         Parser.doAssert(ExpressionNode.parse, "expression"),
    #         createNode=createNode
    #     )
    #
    # @staticmethod
    # def _functionCallParser():
    #     def createNode(name, arguments):
    #         node = FunctionCallNode(name.pos)
    #         node.name = name
    #         node.arguments = arguments
    #         return node
    #
    #     return Parser.allOf(
    #         IdentifierNode.identifierParser(),
    #         ArgumentsListNode.parse,
    #         createNode=createNode
    #     )
    #
    # @staticmethod
    # def identifierParser():
    #     return Parser.terminalParser(TokenType.IDENTIFIER, lambda val, pos: IdentifierNode.withValue(val, pos))
