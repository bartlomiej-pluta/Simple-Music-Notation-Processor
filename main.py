from Tokenizer import tokenize
from Parser import parse
from Evaluator import evaluate
from Environment import createEnvironment
from Error import SyntaxException, RuntimeException
import sys

if __name__ == "__main__":
    try:
        with open(sys.argv[1], 'r') as source:
            lines = [line.rstrip('\n') for line in source.readlines()]
        
        env = createEnvironment()
        
        tokens = tokenize(lines)
        
        ast = parse(tokens)
        
        evaluate(ast, env)
    except SyntaxException as e:
        print(e.msg)
    except RuntimeException as e:
        print(e.msg)
    except KeyboardInterrupt:
        print("Program interrupted")
