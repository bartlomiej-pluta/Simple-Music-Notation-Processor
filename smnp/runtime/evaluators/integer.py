from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class IntegerEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.integer(node.value)