from smnp.ast.node.operator import BinaryOperator, Operator, UnaryOperator
from smnp.ast.node.unit import UnitParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType

class NotOperator(UnaryOperator):
    pass


class Power(BinaryOperator):
    pass

def FactorParser(input):
    from smnp.ast.node.expression import ExpressionParser

    parentheses = Parser.allOf(
        Parser.terminal(TokenType.OPEN_PAREN),
        Parser.doAssert(ExpressionParser, "expression"),
        Parser.terminal(TokenType.CLOSE_PAREN),
        createNode=lambda open, expr, close: expr,
        name="grouping parentheses"
    )

    factorOperands = Parser.oneOf(
        parentheses,
        UnitParser,
        name="factor operands"
    )

    powerFactor = Parser.leftAssociativeOperatorParser(
        factorOperands,
        [TokenType.DOUBLE_ASTERISK],
        factorOperands,
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
