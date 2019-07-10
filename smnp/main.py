from smnp.ast.node.bool import BoolLiteralNode
from smnp.error.base import SmnpException
from smnp.token.tokenizer import tokenize


def main():
    try:
        tokens = tokenize([ "true == true == false.not.not" ])
        BoolLiteralNode.parse(tokens).node.print()
        #stdLibraryEnv = loadStandardLibrary()
        #Interpreter.interpretFile(sys.argv[1], printTokens=False, printAst=True, baseEnvironment=None)

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
