from smnp.newast.node.model import Node
from smnp.newast.parser import Parser


class StatementNode(Node):

    @classmethod
    def _parse(cls, input):
        from smnp.newast.node.block import BlockNode
        from smnp.newast.node.function import FunctionDefinition
        from smnp.newast.node.expression import ExpressionNode
        from smnp.newast.node.ret import ReturnNode

        return Parser.oneOf(
            BlockNode.parse,
            FunctionDefinition.parse,
            ReturnNode.parse,
            ExpressionNode.parse
        )(input)