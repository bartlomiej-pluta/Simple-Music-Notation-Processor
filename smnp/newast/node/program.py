from smnp.error.syntax import SyntaxException
from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.extend import ExtendNode
from smnp.newast.node.function import FunctionDefinitionNode
from smnp.newast.node.model import Node, ParseResult
from smnp.newast.node.statement import StatementNode
from smnp.newast.parser import Parser


class Program(Node):
    def __init__(self):
        super().__init__((-1, -1))

    @classmethod
    def _parse(cls, input):
        def parseToken(input):
            return Parser.oneOf(
                FunctionDefinitionNode.parse,
                ExtendNode.parse,
                ExpressionNode.parse,
                StatementNode.parse,
                exception = SyntaxException(f"Unknown statement: {input.current().pos}")
            )(input)

        root = Program()
        while input.hasCurrent():
            result = parseToken(input)
            if result.result:
                root.append(result.node)
        return ParseResult.OK(root)