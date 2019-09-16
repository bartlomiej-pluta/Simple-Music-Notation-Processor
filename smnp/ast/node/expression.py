from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.operator import BinaryOperator, Operator
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


class Loop(BinaryOperator):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.extend([NoneNode(), NoneNode()])

    @property
    def parameters(self):
        return self[3]

    @parameters.setter
    def parameters(self, value):
        self[3] = value

    @property
    def filter(self):
        return self[4]

    @filter.setter
    def filter(self, value):
        self[4] = value

    @classmethod
    def loop(cls, left, parameters, operator, right, filter):
        node = cls(left.pos)
        node.left = left
        node.parameters = parameters
        node.operator = operator
        node.right = right
        node.filter = filter
        return node


class LoopParameters(Node):
    pass


def ExpressionWithoutLoopParser(input):
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


def LoopParser(input):
    from smnp.ast.node.identifier import IdentifierLiteralParser
    from smnp.ast.node.iterable import abstractIterableParser
    from smnp.ast.node.statement import StatementParser

    loopParameters = Parser.allOf(
        Parser.terminal(TokenType.AS),
        Parser.oneOf(
            Parser.wrap(IdentifierLiteralParser, lambda id: LoopParameters.withChildren([id], id.pos)),
            abstractIterableParser(LoopParameters, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, IdentifierLiteralParser)
        ),
        createNode=lambda asKeyword, parameters: parameters,
        name="loop parameters"
    )

    loopFilter = Parser.allOf(
        Parser.terminal(TokenType.PERCENT),
        Parser.doAssert(ExpressionWithoutLoopParser, "filter as bool expression"),
        createNode=lambda percent, expr: expr,
        name="loop filter"
    )

    return Parser.allOf(
        ExpressionWithoutLoopParser,
        Parser.optional(loopParameters),
        Parser.terminal(TokenType.CARET, createNode=Operator.withValue),
        StatementParser,
        Parser.optional(loopFilter),
        createNode=Loop.loop,
        name="caret-loop"
    )(input)


def ExpressionParser(input):
    return Parser.oneOf(
        LoopParser,
        ExpressionWithoutLoopParser
    )(input)
