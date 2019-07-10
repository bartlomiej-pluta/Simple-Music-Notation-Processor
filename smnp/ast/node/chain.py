from smnp.ast.node.atom import AtomParser
from smnp.ast.node.list import ListParser
from smnp.ast.node.map import MapParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Chain(Valuable):
    pass

itemParser = Parser.oneOf(
    ListParser,
    MapParser,
    AtomParser,
)

ChainParser = Parser.leftAssociativeOperatorParser(itemParser, [TokenType.DOT], itemParser,
                                                   lambda left, op, right: Chain.withValue(BinaryOperator.withValues(left, op, right)))

