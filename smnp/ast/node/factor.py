from smnp.ast.node.operator import BinaryOperator, Operator, UnaryOperator
from smnp.ast.node.unit import UnitParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType

class NotOperator(UnaryOperator):
    pass


class Power(BinaryOperator):
    pass

def FactorParser(input):

    powerFactor = Parser.leftAssociativeOperatorParser(
        UnitParser,
        [TokenType.DOUBLE_ASTERISK],
        UnitParser,
        lambda left, op, right: Power.withValues(left, op, right),
        name="power operator"
    )

    notOperator = Parser.allOf(
        Parser.terminal(TokenType.NOT, Operator.withValue),
        powerFactor,
        createNode=NotOperator.withValues,
        name="not"
    )

    return Parser.oneOf(
        notOperator,
        powerFactor,
        name="factor"
    )(input)
