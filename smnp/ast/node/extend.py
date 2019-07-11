from smnp.ast.node.block import Block
from smnp.ast.node.function import FunctionDefinitionParser
from smnp.ast.node.identifier import IdentifierLiteralParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.type import TypeParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Extend(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

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

    @property
    def methods(self):
        return self[2]

    @methods.setter
    def methods(self, value):
        self[2] = value

    @classmethod
    def withValues(cls, pos, type, variable, methods):
        node = cls(pos)
        node.type = type
        node.variable = variable
        node.methods = methods
        return node

def ExtendParser(input):
    return Parser.allOf(
        Parser.terminal(TokenType.EXTEND),
        TypeParser,
        Parser.terminal(TokenType.AS),
        IdentifierLiteralParser,
        MethodsDeclarationParser,
        createNode=lambda extend, type, _, variable, methods: Extend.withValues(extend.pos, type, variable, methods),
        name="extend"
    )(input)


def MethodsDeclarationParser(input):
    return Parser.loop(
        Parser.terminal(TokenType.OPEN_CURLY),
        FunctionDefinitionParser,
        Parser.terminal(TokenType.CLOSE_CURLY),
        createNode=lambda open, methods, close: Block.withChildren(methods, open.pos),
        name="methods block"
    )(input)

