from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.token.type import TokenType


class List(Node):
    pass


def ListParser(input):
    from smnp.ast.node.expression import ExpressionParser
    return abstractIterableParser(List, TokenType.OPEN_SQUARE, TokenType.CLOSE_SQUARE,
                                    ExpressionParser)(input)
