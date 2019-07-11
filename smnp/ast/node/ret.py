from smnp.ast.node.expression import ExpressionParser
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Return(Valuable):
    pass


def ReturnParser(input):
    return Parser.allOf(
        Parser.terminal(TokenType.RETURN),
        Parser.optional(ExpressionParser),
        createNode=lambda ret, val: Return.withValue(val, ret.pos),
        name="return"
    )(input)