from smnp.ast.parser import parse
from smnp.environment.environment import Environment
from smnp.error.runtime import RuntimeException
from smnp.module import functions, methods
from smnp.program.FileReader import readLines
from smnp.runtime.evaluator import evaluate
from smnp.token.tokenizer import tokenize


class Interpreter:

    @staticmethod
    def interpretString(string, source, printTokens=False, printAst=False, execute=True, baseEnvironment=None):
        return Interpreter._interpret(
            string.splitlines(),
            source,
            printTokens,
            printAst,
            execute,
            baseEnvironment,
        )

    @staticmethod
    def interpretFile(file, printTokens=False, printAst=False, execute=True, baseEnvironment=None, source=None):
        return Interpreter._interpret(
            readLines(file),
            source if source is not None else file,
            printTokens,
            printAst,
            execute,
            baseEnvironment,
        )

    @staticmethod
    def _interpret(lines, source, printTokens=False, printAst=False, execute=True, baseEnvironment=None):
        environment = Environment([{}], functions, methods, source=source)

        if baseEnvironment is not None:
            environment.extend(baseEnvironment)

        try:
            tokens = tokenize(lines)
            if printTokens:
                print(tokens)

            ast = parse(tokens)
            if printAst:
                ast.print()

            if execute:
                evaluate(ast, environment)

            return environment
        except RuntimeException as e:
            e.environment = environment
            e.file = environment.source
            raise e