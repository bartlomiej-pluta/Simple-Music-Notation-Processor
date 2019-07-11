from smnp.ast.node.list import ListParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parsers
from smnp.token.type import TokenType
from smnp.util.singleton import SingletonParser


class Chain(Valuable):
    pass



@SingletonParser
def ChainParser():
    from smnp.ast.node.atom import AtomParser

    itemParser = Parsers.oneOf(
        ListParser,
        #MapParser,
        AtomParser,
        name="chainItem"
    )

    return Parsers.leftAssociativeOperatorParser(
        itemParser,
        [TokenType.DOT],
        itemParser,
        lambda left, op, right: Chain.withValue(BinaryOperator.withValues(left, op, right)),
        name="chain"
    )

