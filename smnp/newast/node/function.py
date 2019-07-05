from smnp.newast.node.block import BlockNode
from smnp.newast.node.identifier import IdentifierNode
from smnp.newast.node.iterable import abstractIterableParser
from smnp.newast.node.model import Node
from smnp.newast.node.none import NoneNode
from smnp.newast.node.statement import StatementNode
from smnp.newast.node.variable import TypedVariableNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class ArgumentsDeclarationNode(Node):

    @classmethod
    def _parse(cls, input):
        raise RuntimeError("This class is not supposed to be automatically called")


class FunctionDefinitionNode(StatementNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

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

    @property
    def body(self):
        return self[2]

    @body.setter
    def body(self, value):
        self[2] = value

    @classmethod
    def _parse(cls, input):
        def createNode(function, name, arguments, body):
            node = FunctionDefinitionNode(function.pos)
            node.name = name
            node.arguments = arguments
            node.body = body
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.FUNCTION),
            IdentifierNode.identifierParser(),
            cls._argumentsDeclarationParser(),
            BlockNode.parse,
            createNode=createNode
        )(input)

    @staticmethod
    def _argumentsDeclarationParser():
        return abstractIterableParser(ArgumentsDeclarationNode, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, TypedVariableNode.parser())