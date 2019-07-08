from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type
from smnp.type.value import Value


class IntegerEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Value(Type.INTEGER, node.value)