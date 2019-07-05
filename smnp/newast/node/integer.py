from smnp.newast.node.access import AccessNode
from smnp.newast.node.expression import ExpressionNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class IntegerLiteralNode(ExpressionNode):

    @classmethod
    def _parse(cls, input):
        def createNode(left, right):
            node = AccessNode(right.pos)
            node.value = left
            node.next = right
            return node

        return Parser.leftAssociativeOperatorParser(
            IntegerLiteralNode._parseInteger(),
            TokenType.DOT,
            IntegerLiteralNode._parseAccessingProperty(),
            createNode=createNode
        )(input)


    @staticmethod
    def _parseInteger():
        createNode = lambda v, pos: IntegerLiteralNode.withValue(v, pos)
        return Parser.terminalParser(TokenType.INTEGER, createNode)

    @staticmethod
    def _parseAccessingProperty():
        # TODO: Just for example. It is supposed to be functionCall (and identifier there)
        return IntegerLiteralNode._parseInteger()
