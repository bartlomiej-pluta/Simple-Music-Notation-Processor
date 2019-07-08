from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import evaluateExpression
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.type.model import Type
from smnp.type.value import Value


class ListEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        list = abstractIterableEvaluator(evaluateExpression)(node, environment)
        return Value(Type.LIST, list)
