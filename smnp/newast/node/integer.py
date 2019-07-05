from smnp.newast.node.expression import ExpressionNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class IntegerLiteralNode(ExpressionNode):

    @classmethod
    def _parse(cls, input):
        createNode = lambda v, pos: IntegerLiteralNode.withValue(v, pos)
        return Parser.terminalParser(TokenType.INTEGER, createNode)(input)