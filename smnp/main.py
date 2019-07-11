from smnp.ast.node.model import Node
from smnp.ast.parser import TerminalParser, OneOfParser, AllOfParser
from smnp.error.base import SmnpException
from smnp.token.tokenizer import tokenize
from smnp.token.type import TokenType


def main():
    try:
        #stdLibraryEnv = loadStandardLibrary()
        #Interpreter.interpretFile(sys.argv[1], printTokens=True, printAst=True, execute=False, baseEnvironment=None)
        #draft()

        def node(*items):
            n = Node((-1, -1))
            n.children = items
            return n

        tokens = tokenize(['=x'])
        parser = AllOfParser(
            OneOfParser(
                TerminalParser(TokenType.ASSIGN),
                TerminalParser(TokenType.ASTERISK),
                name="assignOrAsterisk"
            ),
            TerminalParser(TokenType.INTEGER),
            name="aoaInt",
            createNode=node
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
