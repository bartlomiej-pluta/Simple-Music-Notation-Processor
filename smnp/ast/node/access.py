from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parser
from smnp.error.syntax import SyntaxException
from smnp.token.type import TokenType


class AccessNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [ NoneNode(), NoneNode() ]

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
    def accessParser(cls):
        def createNode(left, operator, right):
            node = AccessNode(right.pos)
            node.left = left
            node.right = right
            return node

        return Parser.leftAssociativeOperatorParser(
            cls._accessLhs(),
            TokenType.DOT,
            cls._accessRhs(),
            createNode=createNode
        )

    @classmethod
    def _accessLhs(cls):
        raise RuntimeError(f"_accessLhs() is not implemented in {cls.__name__} class")

    @staticmethod
    def _accessRhs():
        from smnp.ast.node.identifier import IdentifierNode

        return Parser.oneOf(
            IdentifierNode.functionCallParser(),
            IdentifierNode.identifierParser(),
            exception=lambda input: SyntaxException(f"Expected property name or method call, found '{input.current().rawValue}'", input.currentPos())
        )
