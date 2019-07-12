from smnp.ast.node.block import BlockParser
from smnp.ast.node.identifier import IdentifierLiteralParser
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.type import TypeParser, Type
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ArgumentsDeclaration(Node):
    pass


class Argument(Node):

    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), False]

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
    def vararg(self):
        return self[2]


    @vararg.setter
    def vararg(self, value):
        self[2] = value


class VarargNode(Node):
    pass


class FunctionDefinition(Node):
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
    def withValues(cls, name, arguments, body):
        node = cls(name.pos)
        node.name = name
        node.arguments = arguments
        node.body = body
        return node


def ArgumentParser(input):
    def createNode(type, variable, vararg):
        pos = type.pos if isinstance(type, Type) else variable.pos
        node = Argument(pos)
        node.type = type
        node.variable = variable
        node.vararg = vararg is True
        return node

    return Parser.allOf(
        Parser.optional(TypeParser),
        Parser.doAssert(IdentifierLiteralParser, "argument name"),
        Parser.optional(Parser.terminal(TokenType.DOTS, lambda val, pos: True)),
        createNode=createNode,
        name="function argument"
    )(input)


def ArgumentsDeclarationParser(input):
    return abstractIterableParser(
        ArgumentsDeclaration,
        TokenType.OPEN_PAREN,
        TokenType.CLOSE_PAREN,
        Parser.doAssert(ArgumentParser, "function/method argument")
    )(input)


def FunctionDefinitionParser(input):
    return Parser.allOf(
        Parser.terminal(TokenType.FUNCTION),
        Parser.doAssert(IdentifierLiteralParser, "function/method name"),
        Parser.doAssert(ArgumentsDeclarationParser, "function/method arguments"),
        Parser.doAssert(BlockParser, "function/method body"),
        createNode=lambda _, name, args, body: FunctionDefinition.withValues(name, args, body),
        name="function definition"
    )(input)

