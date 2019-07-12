from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.term import TermParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Sum(BinaryOperator):
    pass


class Relation(BinaryOperator):
    pass


class And(BinaryOperator):
    pass


class Or(BinaryOperator):
    pass


def ExpressionParser(input):
    expr1 = Parser.leftAssociativeOperatorParser(
        TermParser,
        [TokenType.PLUS, TokenType.MINUS],
        TermParser,
        lambda left, op, right: Sum.withValues(left, op, right)
    )

    expr2 = Parser.leftAssociativeOperatorParser(
        expr1,
        [TokenType.RELATION, TokenType.OPEN_ANGLE, TokenType.CLOSE_ANGLE],
        expr1,
        lambda left, op, right: Relation.withValues(left, op, right)
    )

    expr3 = Parser.leftAssociativeOperatorParser(
        expr2,
        [TokenType.AND],
        expr2,
        lambda left, op, right: And.withValues(left, op, right)
    )

    return Parser.leftAssociativeOperatorParser(
        expr3,
        [TokenType.OR],
        expr3,
        lambda left, op, right: Or.withValues(left, op, right)
    )(input)

