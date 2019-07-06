import sys

from smnp.ast.node.program import Program
from smnp.environment.factory import createEnvironment
from smnp.error.base import SmnpException
from smnp.runtime.evaluator import evaluate
from smnp.token.tokenizer import tokenize


def main():
    try:
        with open(sys.argv[1], 'r') as source:
            lines = [line.rstrip('\n') for line in source.readlines()]

        tokens = tokenize(lines)

        ast = Program.parse(tokens)
        ast.node.print()


        env = createEnvironment()

        evaluate(ast, env)

    except SmnpException as e:
        print(e.message())
    except KeyboardInterrupt:
        print("Program interrupted")
