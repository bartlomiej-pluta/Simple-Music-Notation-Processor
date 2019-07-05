from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.iterable import abstractIterableParser
from smnp.token.type import TokenType


class ListNode(ExpressionNode):

    @classmethod
    def _parse(cls, input):
        return abstractIterableParser(ListNode, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, ExpressionNode.parse)(input)
