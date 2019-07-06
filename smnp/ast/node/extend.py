from smnp.ast.node.block import BlockNode
from smnp.ast.node.function import FunctionDefinitionNode
from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.none import NoneNode
from smnp.ast.node.statement import StatementNode
from smnp.ast.node.type import TypeNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ExtendNode(StatementNode):
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
    def _parse(cls, input):
        def createNode(extend, type, asKeyword, variable, methods):
            node = ExtendNode(extend.pos)
            node.type = type
            node.variable = variable
            node.methods = methods
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.EXTEND),
            Parser.doAssert(TypeNode.parse, "type being extended"),
            Parser.terminalParser(TokenType.AS, doAssert=True),
            Parser.doAssert(IdentifierNode.identifierParser(), "variable name"),
            Parser.doAssert(cls._methodsDeclarationsParser(), "methods declarations"),
            createNode=createNode
        )(input)

    @classmethod
    def _methodsDeclarationsParser(cls):
        def createNode(openBracket, items, closeBracket):
            node = BlockNode(openBracket.pos)
            node.children = items
            return node

        return Parser.loop(
            Parser.terminalParser(TokenType.OPEN_CURLY),
            Parser.doAssert(FunctionDefinitionNode.parse, f"method declaration or '{TokenType.CLOSE_CURLY.key}'"),
            Parser.terminalParser(TokenType.CLOSE_CURLY),
            createNode=createNode
        )