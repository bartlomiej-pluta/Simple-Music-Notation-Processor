from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.operator import BinaryOperator, Operator, UnaryOperator
from smnp.ast.node.unit import UnitParser
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Factor(Valuable):
    pass


class NotOperator(UnaryOperator):
    pass


class Loop(BinaryOperator):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(NoneNode())

    @property
    def parameters(self):
        return self[3]

    @parameters.setter
    def parameters(self, value):
        self[3] = value

    @classmethod
    def loop(cls, left, parameters, operator, right):
        node = cls(left.pos)
        node.left = left
        node.parameters = parameters
        node.operator = operator
        node.right = right
        return node


class LoopParameters(Node):
    pass


def FactorParser(input):
    from smnp.ast.node.expression import ExpressionParser
    from smnp.ast.node.statement import StatementParser
    from smnp.ast.node.identifier import IdentifierLiteralParser

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
        lambda left, op, right: Factor.withValue(BinaryOperator.withValues(left, op, right)),
        name="power operator"
    )

    notOperator = Parser.allOf(
        Parser.terminal(TokenType.NOT, Operator.withValue),
        powerFactor,
        createNode=NotOperator.withValues,
        name="not"
    )

    loopParameters = Parser.allOf(
        Parser.terminal(TokenType.AS),
        Parser.oneOf(
            Parser.wrap(IdentifierLiteralParser, lambda id: LoopParameters.withChildren([id], id.pos)),
            abstractIterableParser(LoopParameters, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN, IdentifierLiteralParser)
        ),
        createNode=lambda asKeyword, parameters: parameters,
        name="loop parameters"
    )

    loopFactor = Parser.allOf(
        powerFactor,
        Parser.optional(loopParameters),
        Parser.terminal(TokenType.DASH, createNode=Operator.withValue),
        StatementParser,
        createNode=Loop.loop,
        name="dash-loop"
    )

    return Parser.oneOf(
        loopFactor,
        notOperator,
        powerFactor,
        name="factor"
    )(input)
