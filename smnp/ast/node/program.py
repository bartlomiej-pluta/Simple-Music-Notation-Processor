from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.extend import ExtendNode
from smnp.ast.node.function import FunctionDefinitionNode
from smnp.ast.node.imports import ImportNode
from smnp.ast.node.model import Node, ParseResult
from smnp.ast.node.statement import StatementNode
from smnp.ast.parser import Parser
from smnp.error.syntax import SyntaxException


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
                ImportNode.parse,
                StatementNode.parse,
                exception = SyntaxException(f"Invalid statement: {input.currentToEndOfLine()}", input.current().pos)
            )(input)

        root = Program()
        while input.hasCurrent():
            result = parseToken(input)
            if result.result:
                root.append(result.node)
        return ParseResult.OK(root)