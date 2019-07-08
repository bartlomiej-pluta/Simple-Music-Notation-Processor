from smnp.ast.parser import parse
from smnp.environment.factory import createEnvironment
from smnp.program.FileReader import readLines
from smnp.runtime.evaluator import evaluate
from smnp.token.tokenizer import tokenize


class Interpreter:

    @staticmethod
    def interpretFile(file, printTokens=False, printAst=False):
        lines = readLines(file)

        tokens = tokenize(lines)
        if printTokens:
            print(tokens)

        ast = parse(tokens)
        if printAst:
            ast.print()

        environment = createEnvironment()

        evaluate(ast, environment)

        return environment