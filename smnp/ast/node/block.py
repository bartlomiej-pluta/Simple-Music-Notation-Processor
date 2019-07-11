from smnp.ast.node.model import Node
from smnp.ast.node.statement import StatementParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Block(Node):
    pass


def BlockParser(input):
    return Parser.loop(
        Parser.terminal(TokenType.OPEN_CURLY),
        Parser.doAssert(StatementParser, f"statement or '{TokenType.CLOSE_CURLY.key}'"),
        Parser.terminal(TokenType.CLOSE_CURLY),
        createNode=lambda open, statements, close: Block.withChildren(statements, open.pos)
    )(input)
