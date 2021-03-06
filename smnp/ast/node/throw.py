from smnp.ast.node.expression import ExpressionParser
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Throw(Valuable):
    pass


def ThrowParser(input):
    return Parser.allOf(
        Parser.terminal(TokenType.THROW),
        Parser.doAssert(ExpressionParser, "error message as string"),
        createNode=lambda throw, message: Throw.withValue(message, throw.pos),
        name="throw"
    )(input)