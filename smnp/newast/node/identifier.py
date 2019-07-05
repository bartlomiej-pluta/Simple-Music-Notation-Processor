from smnp.newast.node.access import AccessNode
from smnp.newast.node.args import ArgumentsListNode
from smnp.newast.node.invocation import FunctionCall
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class IdentifierNode(AccessNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]

    @classmethod
    def _literalParser(cls):
        return Parser.oneOf(
            IdentifierNode._functionCallParser(),
            IdentifierNode._identifierParser()
        )

    @staticmethod
    def _functionCallParser():
        def createNode(name, arguments):
            node = FunctionCall(name.pos)
            node.name = name
            node.arguments = arguments
            return node

        return Parser.allOf(
            IdentifierNode._identifierParser(),
            ArgumentsListNode.parse,
            createNode=createNode
        )

    @staticmethod
    def _identifierParser():
        return Parser.terminalParser(TokenType.IDENTIFIER, lambda val, pos: IdentifierNode.withValue(val, pos))
