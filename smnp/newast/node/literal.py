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
        createNode = lambda v, pos: cls.withValue(cls._processValue(v), pos)
        return Parser.terminalParser(cls._getTokenType(), createNode)
