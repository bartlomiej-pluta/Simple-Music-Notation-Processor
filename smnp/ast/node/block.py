from smnp.ast.node.model import Node
from smnp.ast.node.statement import StatementParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Block(Node):
    pass


def BlockParser(input):
    parser = Parser.loop(
        Parser.terminalParser(TokenType.OPEN_CURLY),
        Parser.doAssert(StatementParser, f"statement or '{TokenType.CLOSE_CURLY.key}'"),
        Parser.terminalParser(TokenType.CLOSE_CURLY),
        createNode=lambda open, statements, close: Block.withChildren(statements, open.pos)
    )

    return Parser(parser, "block", [parser])(input)
