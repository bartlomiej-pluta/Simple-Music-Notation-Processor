from smnp.ast.node.atom import AtomParser
from smnp.ast.node.chain import ChainParser
from smnp.ast.node.list import ListParser
from smnp.ast.node.model import Node
from smnp.error.base import SmnpException
from smnp.token.tokenizer import tokenize


def main():
    try:
        # stdLibraryEnv = loadStandardLibrary()
        # Interpreter.interpretFile(sys.argv[1], printTokens=True, printAst=True, execute=False, baseEnvironment=None)
        # draft()

        class TestNode(Node):
            def __init__(self, children):
                super().__init__((-1, -1))
                self.children = children

        tokens = tokenize(['[1, 2]'])
        parser = ListParser()
        #print(parser.grammar())
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
