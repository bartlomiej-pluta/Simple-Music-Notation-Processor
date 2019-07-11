from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.term import TermParser
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Expression(Valuable):
    pass


def ExpressionParser(input):
    from smnp.ast.node.condition import IfElse

    expr1 = Parser.leftAssociativeOperatorParser(
        TermParser,
        [TokenType.PLUS, TokenType.MINUS],
        TermParser,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )

    expr2 =  Parser.leftAssociativeOperatorParser(
        expr1,
        [TokenType.RELATION],
        expr1,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )


    expr3 = Parser.leftAssociativeOperatorParser(
        expr2,
        [TokenType.AND],
        expr2,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )


    expr4 = Parser.leftAssociativeOperatorParser(
        expr3,
        [TokenType.OR],
        expr3,
        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right))
    )

    ifElseExpression = Parser.allOf(
        expr4,
        Parser.terminalParser(TokenType.IF),
        expr4,
        Parser.terminalParser(TokenType.ELSE),
        expr4,
        createNode=lambda ifNode, _, condition, __, elseNode: IfElse.createNode(ifNode, condition, elseNode)
    )

    return Parser.oneOf(
        ifElseExpression,
        expr4,
    )(input)

