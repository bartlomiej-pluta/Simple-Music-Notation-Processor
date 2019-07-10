from smnp.ast.node.atom import AtomParser
from smnp.ast.node.list import ListParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Chain(BinaryOperator):
    pass

itemParser = Parser.oneOf(
    ListParser,
    AtomParser,
)

ChainParser = Parser.leftAssociativeOperatorParser(itemParser, [TokenType.DOT], itemParser,
                                                   lambda left, op, right: Chain.withValues(left, op, right))

