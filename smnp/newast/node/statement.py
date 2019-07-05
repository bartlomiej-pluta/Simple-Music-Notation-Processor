from smnp.newast.node.model import Node
from smnp.newast.parser import Parser


class StatementNode(Node):

    @classmethod
    def _parse(cls, input):
        from smnp.newast.node.block import BlockNode
        from smnp.newast.node.expression import ExpressionNode

        return Parser.oneOf(
            BlockNode.parse,
            ExpressionNode.parse
        )(input)