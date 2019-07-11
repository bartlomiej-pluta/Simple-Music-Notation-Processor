from smnp.ast.node.atom import AtomParser
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.token.type import TokenType


class List(Node):
    pass


def ListParser():
    return abstractIterableParser(List, TokenType.OPEN_SQUARE, TokenType.CLOSE_SQUARE, AtomParser(), name="list")
                                    #MaxPrecedenceExpressionParser)(input)
