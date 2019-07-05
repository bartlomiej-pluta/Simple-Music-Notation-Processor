from smnp.newast.node.expression import ExpressionNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class NoteLiteralNode(ExpressionNode):

    @classmethod
    def _parse(cls, input):
        return Parser.terminalParser(TokenType.NOTE, lambda v, pos: NoteLiteralNode.withValue(v, pos))(input)