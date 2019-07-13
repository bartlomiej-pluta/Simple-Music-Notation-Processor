from smnp.ast.node.model import Node
from smnp.ast.parser import Parser


class Statement(Node):
    pass


def StatementParser(input):
    from smnp.ast.node.block import BlockParser
    from smnp.ast.node.condition import IfElseStatementParser
    from smnp.ast.node.expression import ExpressionParser
    from smnp.ast.node.ret import ReturnParser
    from smnp.ast.node.throw import ThrowParser

    return Parser.oneOf(
        IfElseStatementParser,
        ExpressionParser,
        BlockParser,
        ReturnParser,
        ThrowParser,
        name="statement"
    )(input)
