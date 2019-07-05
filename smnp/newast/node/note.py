from smnp.newast.node.access import AccessNode
from smnp.newast.node.literal import LiteralNode
from smnp.token.type import TokenType


class NoteLiteralNode(LiteralNode, AccessNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]

    @classmethod
    def _getTokenType(cls):
        return TokenType.NOTE