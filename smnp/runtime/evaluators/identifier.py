from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator


class IdentifierEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        try:
            return environment.findVariable(node.value)
        except RuntimeException as e:
            e.pos = node.pos
            raise e
