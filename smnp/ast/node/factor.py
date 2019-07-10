from smnp.ast.node.chain import ChainParser
from smnp.ast.node.operator import BinaryOperator, Operator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Factor(Valuable):
    pass


class Loop(BinaryOperator):
    pass


def FactorParser(input):
    from smnp.ast.node.expression import MaxPrecedenceExpressionParser

    powerFactor = Parser.leftAssociativeOperatorParser(
        ChainParser,
        [TokenType.DOUBLE_ASTERISK],
        ChainParser,
        lambda left, op, right: Factor.withValue(BinaryOperator.withValues(left, op, right))
    )

    exprFactor = Parser.allOf(
        Parser.terminalParser(TokenType.OPEN_PAREN),
        MaxPrecedenceExpressionParser,
        Parser.terminalParser(TokenType.CLOSE_PAREN),
        createNode=lambda open, expr, close: expr
    )

    loopFactor = Parser.allOf(
        powerFactor,
        Parser.terminalParser(TokenType.DASH, lambda val, pos: Operator.withValue(val, pos)),
        MaxPrecedenceExpressionParser, #TODO statement here
        createNode=lambda chain, dash, stmt: Loop.withValues(chain, dash, stmt)
    )

    return Parser.oneOf(
        loopFactor,
        powerFactor,
        exprFactor,
    )(input)
