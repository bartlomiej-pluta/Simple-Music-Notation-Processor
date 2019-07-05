from smnp.newast.node.expression import ExpressionNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class StringLiteralNode(ExpressionNode):

    @classmethod
    def _parse(cls, input):
        createNode = lambda v, pos: StringLiteralNode.withValue(pos, v[1:len(v)-1])
        return Parser.terminalParser(TokenType.STRING, createNode)(input)