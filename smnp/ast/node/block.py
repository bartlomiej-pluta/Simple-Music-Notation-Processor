from smnp.ast.node.statement import StatementNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class BlockNode(StatementNode):

    @classmethod
    def _parse(cls, input):
        def createNode(start, items, end):
            node = BlockNode(start.pos)
            node.children = items
            return node

        return Parser.loop(
            Parser.terminalParser(TokenType.OPEN_BRACKET),
            StatementNode.parse,
            Parser.terminalParser(TokenType.CLOSE_BRACKET),
            createNode=createNode
        )(input)