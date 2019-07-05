from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.none import NoneNode
from smnp.newast.node.statement import StatementNode
from smnp.newast.parser import Parser
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
            ExpressionNode.parse,
            createNode=createNode
        )(input)