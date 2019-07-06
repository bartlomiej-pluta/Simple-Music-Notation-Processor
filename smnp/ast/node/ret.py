from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.none import NoneNode
from smnp.ast.node.statement import StatementNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ReturnNode(StatementNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(NoneNode())

    @property
    def value(self):
        return self[0]

    @value.setter
    def value(self, value):
        self[0] = value

    @classmethod
    def _parse(cls, input):
        def createNode(ret, value):
            node = ReturnNode(ret.pos)
            node.value = value
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.RETURN),
            Parser.doAssert(ExpressionNode.parse, "expression"),
            createNode=createNode
        )(input)