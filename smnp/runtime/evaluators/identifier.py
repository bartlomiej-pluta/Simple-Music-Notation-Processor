from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.tools import updatePos


class IdentifierEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        try:
            return environment.findVariable(node.value)
        except RuntimeException as e:
            raise updatePos(e, node)
