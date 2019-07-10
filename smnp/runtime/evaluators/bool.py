from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class BoolEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.bool(node.value)