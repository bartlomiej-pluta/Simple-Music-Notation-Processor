from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.term import TermParser
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Expression(Valuable):
    pass


def ExpressionParser(input):
    return Parser.leftAssociativeOperatorParser(
        TermParser,
        [TokenType.PLUS, TokenType.MINUS],
        TermParser,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )(input)


def Expression2Parser(input):
    return Parser.leftAssociativeOperatorParser(
        ExpressionParser,
        [TokenType.RELATION],
        ExpressionParser,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )(input)


def Expression3Parser(input):
    return Parser.leftAssociativeOperatorParser(
        Expression2Parser,
        [TokenType.AND],
        Expression2Parser,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )(input)


def Expression4Parser(input):
    from smnp.ast.node.condition import IfElse
    exprParser = Parser.leftAssociativeOperatorParser(
        Expression3Parser,
        [TokenType.OR],
        Expression3Parser,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )

    ifElseExpression = Parser.allOf(
        exprParser,
        Parser.terminalParser(TokenType.IF),
        Expression4Parser,
        Parser.terminalParser(TokenType.ELSE),
        Expression4Parser,
        createNode=lambda ifNode, _, condition, __, elseNode: IfElse.createNode(ifNode, condition, elseNode)
    )

    return Parser.oneOf(
        ifElseExpression,
        exprParser,
    )(input)


MaxPrecedenceExpressionParser = Expression4Parser