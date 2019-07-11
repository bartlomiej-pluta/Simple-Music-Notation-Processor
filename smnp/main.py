from smnp.ast.node.model import Node
from smnp.ast.parser import TerminalParser, OneOfParser, AllOfParser, OptionalParser, LoopParser
from smnp.error.base import SmnpException
from smnp.token.tokenizer import tokenize
from smnp.token.type import TokenType


def main():
    try:
        # stdLibraryEnv = loadStandardLibrary()
        # Interpreter.interpretFile(sys.argv[1], printTokens=True, printAst=True, execute=False, baseEnvironment=None)
        # draft()

        class TestNode(Node):
            def __init__(self, children):
                super().__init__((-1, -1))
                self.children = children

        tokens = tokenize(['{*1^*1^}'])
        parser = LoopParser(
            TerminalParser(TokenType.OPEN_CURLY),
            AllOfParser(
                OneOfParser(
                    TerminalParser(TokenType.ASSIGN),
                    TerminalParser(TokenType.ASTERISK),
                    name="assignOrAsterisk"
                ),
                OptionalParser(TerminalParser(TokenType.INTEGER), name="optInt"),
                TerminalParser(TokenType.DASH),
                name="aoaInt",
                createNode=lambda a, b, c: TestNode([a, b, c])
            ),
            TerminalParser(TokenType.CLOSE_CURLY),
            createNode=lambda a, b, c: TestNode([a, b, c]),
            name="block",
        )
        print(parser.grammar())
        res = parser.parse(tokens)

        print()
        if res.result:
            res.node.print()
        else:
            print("nie sparsowano")

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
