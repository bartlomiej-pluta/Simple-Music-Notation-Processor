from smnp.ast.node.atom import AtomParser
from smnp.ast.node.list import ListParser
from smnp.ast.node.map import MapParser
from smnp.ast.node.operator import BinaryOperator, UnaryOperator, Operator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Chain(Valuable):
    pass


class MinusOperator(UnaryOperator):
    pass


def ChainParser(input):
    chain1 = Parser.oneOf(
        ListParser,
        MapParser,
        AtomParser,
    )

    minusOperator = Parser.allOf(
        Parser.terminal(TokenType.MINUS, createNode=Operator.withValue),
        chain1,
        createNode=MinusOperator.withValues,
        name="minus"
    )

    chain2 = Parser.oneOf(
        minusOperator,
        chain1
    )

    return Parser.leftAssociativeOperatorParser(
        chain2,
        [TokenType.DOT],
        chain2,
        lambda left, op, right: Chain.withValue(BinaryOperator.withValues(left, op, right))
    )(input)

