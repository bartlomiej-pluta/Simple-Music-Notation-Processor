from smnp.ast.node.atom import AtomParser
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.token.type import TokenType


class List(Node):
    pass


ListParser = abstractIterableParser(List, TokenType.OPEN_SQUARE, TokenType.CLOSE_SQUARE,
                                    AtomParser)  #TODO -> zamienić na expr czy coś
