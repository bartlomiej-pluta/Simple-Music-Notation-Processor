from smnp.ast.node.access import LeftAssociativeOperatorNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ListNode(LeftAssociativeOperatorNode):

    @classmethod
    def _literalParser(cls):
        return abstractIterableParser(ListNode, TokenType.OPEN_SQUARE, TokenType.CLOSE_SQUARE,
                                      Parser.doAssert(ExpressionNode.parse, "expression"))
