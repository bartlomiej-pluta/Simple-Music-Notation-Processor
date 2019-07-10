from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class RelationOperatorNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [ NoneNode(), NoneNode(), NoneNode()]

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
    def relationParser(cls):
        def createNode(left, operator, right):
            node = RelationOperatorNode(right.pos)
            node.left = left
            node.operator = operator
            node.right = right
            return node

        return Parser.leftAssociativeOperatorParser(
            cls._relationLhs(),
            TokenType.EQUAL,
            cls._relationRhs(),
            createNode=createNode
        )

    @classmethod
    def _relationLhs(cls):
        raise RuntimeError(f"_relationLhs() is not implemented in {cls.__name__} class")

    @staticmethod
    def _relationRhs():
        from smnp.ast.node.bool import BoolLiteralNode
        from smnp.ast.node.identifier import IdentifierNode

        from smnp.ast.node.string import StringLiteralNode
        return Parser.doAssert(Parser.oneOf(
            BoolLiteralNode.accessParser(),
            BoolLiteralNode.literalParser(),
            IdentifierNode.literalParser(),
            StringLiteralNode.accessParser(),
            StringLiteralNode.literalParser()
        ), "expression")