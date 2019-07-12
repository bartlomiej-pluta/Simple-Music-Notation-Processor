from smnp.ast.node.factor import FactorParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Product(BinaryOperator):
    pass


def TermParser(input):
    return Parser.leftAssociativeOperatorParser(
        FactorParser,
        [TokenType.ASTERISK, TokenType.SLASH],
        FactorParser,
        lambda left, op, right: Product.withValues(left, op, right)
    )(input)