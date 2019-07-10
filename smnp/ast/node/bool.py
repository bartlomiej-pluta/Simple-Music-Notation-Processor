from smnp.ast.node.access import AccessNode
from smnp.ast.node.literal import LiteralNode
from smnp.ast.node.relation import RelationOperatorNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class BoolLiteralNode(LiteralNode, AccessNode, RelationOperatorNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]

    @classmethod
    def _getTokenType(cls):
        return TokenType.BOOL

    @classmethod
    def _parse(cls, input):
        x = Parser.oneOf(

            cls.relationParser(),
            cls.accessParser(),
            cls.literalParser()
        )(input)
        return x

    @classmethod
    def _accessLiteralParser(cls):
        return cls.literalParser()

    @classmethod
    def _relationLiteralParser(cls):
        return cls.literalParser()