from smnp.ast.node.type import TypeParser
from smnp.error.base import SmnpException
from smnp.token.tokenizer import tokenize


def main():
    try:
        #stdLibraryEnv = loadStandardLibrary()
        #Interpreter.interpretFile(sys.argv[1], printTokens=True, printAst=True, execute=False, baseEnvironment=None)
        #draft()
        tokens = tokenize(['<list, string>'])
        TypeParser(tokens).node.print()

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
