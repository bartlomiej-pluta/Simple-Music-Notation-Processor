from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode


class BinaryOperator(Node):
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
    def withValues(cls, left, operator, right):
        node = cls(operator.pos)
        node.left = left
        node.operator = operator
        node.right = right
        return node

#
# class LeftAssociativeOperatorNode(ExpressionNode):
#     def __init__(self, pos):
#         super().__init__(pos)
#         self.children = [NoneNode(), NoneNode(), NoneNode()]
#
#     @property
#     def left(self):
#         return self[0]
#
#     @left.setter
#     def left(self, value):
#         self[0] = value
#
#     @property
#     def operator(self):
#         return self[1]
#
#     @operator.setter
#     def operator(self, value):
#         self[1] = value
#
#     @property
#     def right(self):
#         return self[2]
#
#     @right.setter
#     def right(self, value):
#         self[2] = value
#
#     @classmethod
#     def _parse(cls, input):
#         def createNode(left, operator, right):
#             node = LeftAssociativeOperatorNode(right.pos)
#             node.left = left
#             node.operator = operator
#             node.right = right
#             return node
#
#         return Parser.leftAssociativeOperatorParser(
#             cls._lhsParser(),
#             TokenType.DOT,
#             cls._rhsParser(),
#             createNode=createNode
#         )(input)
#
#     @classmethod
#     def _lhsParser(cls):
#         raise RuntimeError(f"LHS parser is not implemented in {cls.__name__}")
#
#     @staticmethod
#     def _rhsParser():
#         from smnp.ast.node.identifier import IdentifierNode
#
#         return Parser.oneOf(
#             # TODO!!!
#             IdentifierNode._lhsParser(),
#             IdentifierNode._functionCallParser(),
#             exception=lambda input: SyntaxException(f"Expected property name or method call, found '{input.current().rawValue}'", input.currentPos())
#         )
#
#
class Operator(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @property
    def value(self):
        return self[0]

    @value.setter
    def value(self, value):
        self[0] = value

    @classmethod
    def withValue(cls, value, pos):
        node = cls(pos)
        node.value = value
        return node