from smnp.ast.node.block import BlockNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.statement import StatementNode
from smnp.ast.node.type import TypeNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ArgumentsDeclarationNode(Node):

    @classmethod
    def _parse(cls, input):
        raise RuntimeError("This class is not supposed to be automatically called")


class ArgumentDefinitionNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(NoneNode())

    @property
    def type(self):
        return self[0]

    @type.setter
    def type(self, value):
        self[0] = value

    @property
    def variable(self):
        return self[1]

    @variable.setter
    def variable(self, value):
        self[1] = value

    @classmethod
    def parser(cls):
        def createNode(type, variable):
            node = ArgumentDefinitionNode(type.pos)
            node.type = type
            node.variable = variable
            return node

        return Parser.allOf(
            TypeNode.parse,
            Parser.doAssert(IdentifierNode.identifierParser(), "variable name"),
            createNode=createNode
        )

    @classmethod
    def _parse(cls, input):
        #TODO
        raise RuntimeError("Not implemented yet. There is still required work to correctly build AST related to IdentifierNode")



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
            Parser.doAssert(IdentifierNode.identifierParser(), "function name"),
            Parser.doAssert(cls._argumentsDeclarationParser(), "arguments list"),
            Parser.doAssert(BlockNode.parse, "function body"),
            createNode=createNode
        )(input)

    @staticmethod
    def _argumentsDeclarationParser():
        return abstractIterableParser(ArgumentsDeclarationNode, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, ArgumentDefinitionNode.parser())