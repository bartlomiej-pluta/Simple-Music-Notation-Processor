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

    simpleExtend = Parser.allOf(
        Parser.terminal(TokenType.EXTEND),
        TypeParser,
        Parser.terminal(TokenType.AS),
        IdentifierLiteralParser,
        Parser.terminal(TokenType.WITH),
        Parser.doAssert(Parser.wrap(FunctionDefinitionParser, lambda method: Block.withChildren([ method ], method.pos)), "method definition"),
        createNode=lambda extend, type, _, variable, __, methods: Extend.withValues(extend.pos, type, variable, methods),
        name="simple extend"
    )

    multiExtend = Parser.allOf(
        Parser.terminal(TokenType.EXTEND),
        Parser.doAssert(TypeParser, "type being extended"),
        Parser.terminal(TokenType.AS, doAssert=True),
        Parser.doAssert(IdentifierLiteralParser, "variable name"),
        Parser.doAssert(MethodsDeclarationParser, f"block with methods definitions or '{TokenType.WITH.key}' keyword"),
        createNode=lambda extend, type, _, variable, methods: Extend.withValues(extend.pos, type, variable, methods),
        name="multiple extend"
    )


    return Parser.oneOf(
        simpleExtend,
        multiExtend,
        name="extend"
    )(input)


def MethodsDeclarationParser(input):
    return Parser.loop(
        Parser.terminal(TokenType.OPEN_CURLY),
        Parser.doAssert(FunctionDefinitionParser, f"method definition or '{TokenType.CLOSE_CURLY.key}'"),
        Parser.terminal(TokenType.CLOSE_CURLY),
        createNode=lambda open, methods, close: Block.withChildren(methods, open.pos),
        name="methods block"
    )(input)

