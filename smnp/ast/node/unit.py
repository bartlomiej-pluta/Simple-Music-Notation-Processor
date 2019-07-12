from smnp.ast.node.atom import AtomParser
from smnp.ast.node.operator import BinaryOperator, UnaryOperator, Operator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Unit(Valuable):
    pass


class MinusOperator(UnaryOperator):
    pass


def UnitParser(input):
    minusOperator = Parser.allOf(
        Parser.terminal(TokenType.MINUS, createNode=Operator.withValue),
        Parser.doAssert(AtomParser, "atom"),
        createNode=MinusOperator.withValues,
        name="minus"
    )

    atom2 = Parser.oneOf(
        minusOperator,
        AtomParser,
        name="atom2"
    )

    return Parser.leftAssociativeOperatorParser(
        atom2,
        [TokenType.DOT],
        Parser.doAssert(atom2, "atom"),
        createNode=lambda left, op, right: Unit.withValue(BinaryOperator.withValues(left, op, right)),
        name="unit"
    )(input)

