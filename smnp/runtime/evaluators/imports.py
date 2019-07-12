from smnp.program.interpreter import Interpreter
from smnp.runtime.evaluator import Evaluator


class ImportEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        source = node.source
        newEnvironment = Interpreter.interpretFile(source.value, baseEnvironment=environment)
        environment.extend(newEnvironment)