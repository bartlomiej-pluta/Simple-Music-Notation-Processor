from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class RelationOperatorNode(ExpressionNode):
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
    def relationParser(cls):
        def createNode(left, right):
            node = RelationOperatorNode(right.pos)
            node.left = left
            node.right = right
            return node

        return Parser.leftAssociativeOperatorParser(
            cls._relationLiteralParser(),
            TokenType.EQUAL,
            cls._parseRelationProperty(),
            createNode=createNode
        )

    @classmethod
    def _relationLiteralParser(cls):
        raise RuntimeError(f"_relationLiteralParser() is not implemented in {cls.__name__} class")

    @staticmethod
    def _parseRelationProperty():
        # TODO doAssert
        return ExpressionNode.parse