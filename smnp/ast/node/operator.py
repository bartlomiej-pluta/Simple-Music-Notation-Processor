from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parser
from smnp.error.syntax import SyntaxException
from smnp.token.type import TokenType


class LeftAssociativeOperatorNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

    @property
    def left(self):
        return self[0]

    @left.setter
    def left(self, value):
        self[0] = value

    @property
    def operator(self):
        return self[1]

    @operator.setter
    def operator(self, value):
        self[1] = value

    @property
    def right(self):
        return self[2]

    @right.setter
    def right(self, value):
        self[2] = value

    @classmethod
    def _parse(cls, input):
        def createNode(left, operator, right):
            node = LeftAssociativeOperatorNode(right.pos)
            node.left = left
            node.operator = operator
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


class OperatorNode(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @property
    def value(self):
        return self[0]

    @value.setter
    def value(self, value):
        self[0] = value