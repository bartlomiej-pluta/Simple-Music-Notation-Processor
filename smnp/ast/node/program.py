from smnp.ast.node.extend import ExtendParser
from smnp.ast.node.function import FunctionDefinitionParser
from smnp.ast.node.imports import ImportParser
from smnp.ast.node.model import Node, ParseResult
from smnp.ast.node.statement import StatementParser
from smnp.ast.parser import Parser
from smnp.error.syntax import SyntaxException


class Program(Node):
    def __init__(self):
        super().__init__((-1, -1))

def ProgramParser(input):
    def parse(input):
        root = Program()

        # Start Symbol
        startSymbolParser = Parser.oneOf(
            ImportParser,
            FunctionDefinitionParser,
            ExtendParser,
            StatementParser,
            exception=lambda inp: SyntaxException(f"Invalid statement: {inp.currentToEndOfLine()}", inp.current().pos),
            name="start symbol"
        )

        while input.hasCurrent():
            result = startSymbolParser(input)

            if result.result:
                root.append(result.node)

        return ParseResult.OK(root)

    return Parser(parse, name="program")(input)
