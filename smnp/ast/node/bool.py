from smnp.ast.node.access import LeftAssociativeOperatorNode
from smnp.ast.node.literal import LiteralNode
from smnp.token.type import TokenType


class BoolLiteralNode(LiteralNode, LeftAssociativeOperatorNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @classmethod
    def _getTokenType(cls):
        return TokenType.BOOL