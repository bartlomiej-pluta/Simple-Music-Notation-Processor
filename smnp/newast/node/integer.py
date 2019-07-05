from smnp.newast.node.access import AccessNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class IntegerLiteralNode(AccessNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]


    @classmethod
    def _literalParser(cls):
        createNode = lambda v, pos: IntegerLiteralNode.withValue(v, pos)
        return Parser.terminalParser(TokenType.INTEGER, createNode)