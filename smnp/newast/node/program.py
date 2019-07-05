from smnp.error.syntax import SyntaxException
from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.model import Node, ParseResult
from smnp.newast.parser import Parser


class Program(Node):
    def __init__(self):
        super().__init__((-1, -1))

    @classmethod
    def _parse(cls, input):
        def parseToken(input):
            return Parser.oneOf(
                ExpressionNode.parse,
                exception = SyntaxException("Unknown statement")
            )(input)

        root = Program()
        while input.hasCurrent():
            result = parseToken(input)
            if result.result:
                root.append(result.node)
        return ParseResult.OK(root)