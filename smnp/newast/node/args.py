from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.iterable import abstractIterableParser
from smnp.newast.node.model import Node
from smnp.token.type import TokenType


class ArgumentsListNode(Node):

    @classmethod
    def _parse(cls, input):
        return abstractIterableParser(ArgumentsListNode, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, ExpressionNode.parse)(input)