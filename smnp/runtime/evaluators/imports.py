from smnp.ast.node.none import NoneNode
from smnp.program.interpreter import Interpreter
from smnp.runtime.evaluator import Evaluator


class ImportEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        if type(node.type) == NoneNode:
            cls._evaluateCodeImport(node, environment)
        else:
            raise RuntimeError("Importing types is not implemented yet")

    @classmethod
    def _evaluateCodeImport(cls, node, environment):
        source = node.source
        newEnvironment = Interpreter.interpretFile(source.value)
        environment.extend(newEnvironment)