from smnp.ast.node.chain import ChainParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Factor(Valuable):
    pass


powerFactor = Parser.leftAssociativeOperatorParser(ChainParser, [TokenType.DOUBLE_ASTERISK], ChainParser,
                                                    lambda left, op, right: Factor.withValue(BinaryOperator.withValues(left, op, right)))


def exprFactor():
    from smnp.ast.node.expression import ExpressionParser

    return Parser.allOf(
        Parser.terminalParser(TokenType.OPEN_PAREN),
        ExpressionParser,
        Parser.terminalParser(TokenType.CLOSE_PAREN),
        createNode=lambda open, expr, close: expr
    )

def FactorParser(input):
    return Parser.oneOf(
        powerFactor,
        exprFactor()
    )(input)
