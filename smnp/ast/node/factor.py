from smnp.ast.node.chain import ChainParser
from smnp.ast.node.operator import BinaryOperator, Operator, UnaryOperator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Factor(Valuable):
    pass


class NotOperator(UnaryOperator):
    pass

class Loop(BinaryOperator):
    pass


def FactorParser(input):
    from smnp.ast.node.expression import ExpressionParser
    from smnp.ast.node.statement import StatementParser

    powerFactor = Parser.leftAssociativeOperatorParser(
        ChainParser,
        [TokenType.DOUBLE_ASTERISK],
        ChainParser,
        lambda left, op, right: Factor.withValue(BinaryOperator.withValues(left, op, right)),
        name="power operator"
    )

    exprFactor = Parser.allOf(
        Parser.terminalParser(TokenType.OPEN_PAREN),
        ExpressionParser,
        Parser.terminalParser(TokenType.CLOSE_PAREN),
        createNode=lambda open, expr, close: expr,
        name="grouping parentheses"
    )

    factorParser = Parser.oneOf(
        powerFactor,
        exprFactor,
        name="basic factor"
    )

    notOperator = Parser.allOf(
        Parser.terminalParser(TokenType.NOT, Operator.withValue),
        factorParser,
        createNode=NotOperator.withValues,
        name="not"
    )

    loopFactor = Parser.allOf(
        factorParser,
        Parser.terminalParser(TokenType.DASH, createNode=Operator.withValue),
        StatementParser,
        createNode=Loop.withValues,
        name="dash-loop"
    )

    return Parser.oneOf(
        loopFactor,
        notOperator,
        factorParser
    )(input)
