from smnp.ast.node.model import Node
from smnp.ast.parser import Parser


class Statement(Node):
    pass


def StatementParser(input):
    from smnp.ast.node.block import BlockParser
    from smnp.ast.node.condition import IfElseStatementParser
    from smnp.ast.node.expression import ExpressionParser

    parser = Parser.oneOf(
        IfElseStatementParser,
        BlockParser,
        ExpressionParser
    )

    return Parser(parser, "statement", parser)(input)
