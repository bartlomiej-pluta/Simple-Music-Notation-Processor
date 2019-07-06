from smnp.ast.node.access import AccessNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.iterable import abstractIterableParser
from smnp.token.type import TokenType


class ListNode(AccessNode):

    @classmethod
    def _literalParser(cls):
        return abstractIterableParser(ListNode, TokenType.OPEN_SQUARE, TokenType.CLOSE_SQUARE, ExpressionNode.parse)
