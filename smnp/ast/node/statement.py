from smnp.ast.node.model import Node
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Statement(Node):
    pass


def StatementParser(input):
    from smnp.ast.node.block import BlockParser
    from smnp.ast.node.condition import IfElseStatementParser
    from smnp.ast.node.expression import ExpressionParser
    from smnp.ast.node.ret import ReturnParser
    from smnp.ast.node.throw import ThrowParser

    return withSemicolon(
        Parser.oneOf(
            IfElseStatementParser,
            ExpressionParser,  # Must be above BlockParser because of Map's syntax with curly braces
            BlockParser,
            ReturnParser,
            ThrowParser,
            name="statement"
        ), optional=True)(input)


def withSemicolon(parser, optional=False, doAssert=False):
    semicolonParser = Parser.optional(Parser.terminal(TokenType.SEMICOLON)) if optional else Parser.terminal(
        TokenType.SEMICOLON, doAssert=doAssert)

    return Parser.allOf(
        parser,
        semicolonParser,
        createNode=lambda stmt, semicolon: stmt,
        name="semicolon" + "?" if optional else ""
    )
