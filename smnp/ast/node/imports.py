from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.string import StringLiteralNode
from smnp.ast.node.type import TypeNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ImportNode(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

    @property
    def source(self):
        return self[0]

    @source.setter
    def source(self, value):
        self[0] = value

    @property
    def type(self):
        return self[1]

    @type.setter
    def type(self, value):
        self[1] = value

    @property
    def variable(self):
        return self[2]

    @variable.setter
    def variable(self, value):
        self[2] = value

    @classmethod
    def _parse(cls, input):
        return Parser.oneOf(
            cls._literalImportParser(),
            cls._fileImportParser()
        )(input)

    @classmethod
    def _literalImportParser(cls):
        def createNode(importKeyword, type, fromKeyword, source, asKeyword, variable):
            node = ImportNode(importKeyword.pos)
            node.source = source
            node.type = type
            node.variable = variable
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.IMPORT),
            TypeNode.parse,
            Parser.doAssert(Parser.terminalParser(TokenType.FROM), "'from <source> as <variable name>'"),
            Parser.doAssert(StringLiteralNode._literalParser(), "source as a string"),
            Parser.doAssert(Parser.terminalParser(TokenType.AS), "'as <variable name>'"),
            Parser.doAssert(IdentifierNode.identifierParser(), "variable name"),
            createNode=createNode
        )

    @classmethod
    def _fileImportParser(cls):
        def createNode(importKeyword, source):
            node = ImportNode(importKeyword.pos)
            node.source = source
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.IMPORT),
            Parser.doAssert(StringLiteralNode._literalParser(), "source as a string"),
            createNode=createNode
        )
