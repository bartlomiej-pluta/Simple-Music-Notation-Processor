from smnp.ast.node.literal import LiteralNode
from smnp.token.type import TokenType


class StringLiteralNode(LiteralNode):
    def __init__(self, pos):
        super().__init__(pos)
        #TODO del self.children[1]


    # TODO: To Remove
    @classmethod
    def _parse(cls, input):
        return cls.literalParser()(input)

    @classmethod
    def _getTokenType(cls):
        return TokenType.STRING