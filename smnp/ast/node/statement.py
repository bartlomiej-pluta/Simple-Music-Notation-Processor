from smnp.ast.node.model import Node
from smnp.ast.parser import Parser


class StatementNode(Node):

    @classmethod
    def _parse(cls, input):
        from smnp.ast.node.block import BlockNode
        from smnp.ast.node.expression import ExpressionNode
        from smnp.ast.node.ret import ReturnNode

        return Parser.oneOf(
            BlockNode.parse,
            ReturnNode.parse,
            ExpressionNode.parse
        )(input)