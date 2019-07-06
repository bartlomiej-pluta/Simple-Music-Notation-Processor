from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.parser import Parser
from smnp.error.syntax import SyntaxException
from smnp.token.type import TokenType


class AccessNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(IgnoredNode(pos))

    @property
    def left(self):
        return self[0]

    @left.setter
    def left(self, value):
        self[0] = value

    @property
    def right(self):
        return self[1]

    @right.setter
    def right(self, value):
        self[1] = value

    @classmethod
    def _parse(cls, input):
        def createNode(left, right):
            node = AccessNode(right.pos)
            node.left = left
            node.right = right
            return node

        return Parser.leftAssociativeOperatorParser(
            cls._literalParser(),
            TokenType.DOT,
            cls._parseAccessingProperty(),
            createNode=createNode
        )(input)

    @classmethod
    def _literalParser(cls):
        pass

    @staticmethod
    def _parseAccessingProperty():
        from smnp.ast.node.identifier import IdentifierNode

        return Parser.oneOf(
            IdentifierNode._literalParser(),
            IdentifierNode._functionCallParser(),
            exception=lambda input: SyntaxException(f"Expected property name or method call, found '{input.current().rawValue}'", input.currentPos())
        )
