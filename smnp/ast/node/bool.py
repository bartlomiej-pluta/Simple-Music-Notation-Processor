from smnp.ast.node.literal import LiteralNode
from smnp.ast.node.operator import LeftAssociativeOperatorNode
from smnp.token.type import TokenType


class BoolLiteralNode(LiteralNode, LeftAssociativeOperatorNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @classmethod
    def _getTokenType(cls):
        return TokenType.BOOL