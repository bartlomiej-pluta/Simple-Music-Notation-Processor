from smnp.ast.node.access import AccessNode
from smnp.ast.node.literal import LiteralNode
from smnp.ast.node.relation import RelationOperatorNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class StringLiteralNode(AccessNode, RelationOperatorNode, LiteralNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]

    @classmethod
    def _parse(cls, input):
        return Parser.oneOf(
            cls.accessParser(),
            cls.relationParser(),
            cls.literalParser()
        )(input)

    @classmethod
    def _accessLhs(cls):
        return cls.literalParser()

    @classmethod
    def _relationLhs(cls):
        return cls.literalParser()

    @classmethod
    def _getTokenType(cls):
        return TokenType.STRING