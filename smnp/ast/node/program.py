from smnp.ast.node.expression import MaxPrecedenceExpressionParser
from smnp.ast.node.model import Node, ParseResult
from smnp.ast.parser import Parser


class Program(Node):
    def __init__(self):
        super().__init__((-1, -1))

def parse(input):
    root = Program()
    while input.hasCurrent():
        result = Parser.oneOf(
            # Start Symbol


            #TODO -> temporary (to remove):
            MaxPrecedenceExpressionParser,
            exception=RuntimeError("Nie znam tego wyrazenia")
        )(input)

        if result.result:
            root.append(result.node)

    return ParseResult.OK(root)

ProgramParser = Parser(parse, name="program")
    # @classmethod
    # def _parse(cls, input):
    #     def parseToken(input):
    #         return Parser.oneOf(
    #             FunctionDefinitionNode.parse,
    #             ExtendNode.parse,
    #             ExpressionNode.parse,
    #             ImportNode.parse,
    #             StatementNode.parse,
    #             exception = SyntaxException(f"Invalid statement: {input.currentToEndOfLine()}", input.current().pos)
    #         )(input)
    #
    #     root = Program()
    #     while input.hasCurrent():
    #         result = parseToken(input)
    #         if result.result:
    #             root.append(result.node)
    #     return ParseResult.OK(root)