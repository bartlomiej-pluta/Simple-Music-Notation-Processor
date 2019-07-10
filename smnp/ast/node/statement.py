from smnp.ast.node.expression import MaxPrecedenceExpressionParser
from smnp.ast.node.model import Node
from smnp.ast.parser import Parser


class Statement(Node):
    pass


def StatementParser(input):
    from smnp.ast.node.block import BlockParser

    parser = Parser.oneOf(
        BlockParser,
        MaxPrecedenceExpressionParser
    )

    return Parser(parser, "statement", parser)(input)

# class StatementNode(Node):
#
#     @classmethod
#     def _parse(cls, input):
#         from smnp.ast.node.block import BlockNode
#         from smnp.ast.node.expression import ExpressionNode
#         from smnp.ast.node.ret import ReturnNode
#
#         return Parser.oneOf(
#             ExpressionNode.parse,
#             BlockNode.parse,
#             ReturnNode.parse,
#         )(input)