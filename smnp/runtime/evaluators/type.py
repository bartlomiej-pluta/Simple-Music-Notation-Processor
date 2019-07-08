from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class TypeEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.type(node.type)