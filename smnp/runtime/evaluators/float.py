from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class FloatEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.float(node.value)