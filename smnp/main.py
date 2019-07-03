import sys
from smnp.error.syntax import SyntaxException
from smnp.error.runtime import RuntimeException
from smnp.token.tokenizer import tokenize
from smnp.ast.parser import parse
#from Tokenizer import tokenize
#from Evaluator import evaluate
#from Environment import createEnvironment
#from Error import SyntaxException, RuntimeException

def main():
    try:
        with open(sys.argv[1], 'r') as source:
            lines = [line.rstrip('\n') for line in source.readlines()]

        #env = createEnvironment()

        tokens = tokenize(lines)

        ast = parse(tokens)

        #evaluate(ast, env)
    except SyntaxException as e:
        print(e.msg)
    except RuntimeException as e:
        print(e.msg)
    except KeyboardInterrupt:
        print("Program interrupted")

