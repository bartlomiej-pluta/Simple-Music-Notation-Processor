from smnp.newast.node.expression import ExpressionNode
from smnp.newast.parser import Parser


class LiteralNode(ExpressionNode):

    @classmethod
    def _getTokenType(cls):
        pass

    @classmethod
    def _processValue(cls, value):
        return value

    @classmethod
    def _literalParser(cls):
        createNode = lambda val, pos: cls.withValue(cls._processValue(val), pos)
        return Parser.terminalParser(cls._getTokenType(), createNode)
