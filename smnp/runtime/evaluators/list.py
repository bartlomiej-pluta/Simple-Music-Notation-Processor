from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.type.model import Type


class ListEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        list = abstractIterableEvaluator(expressionEvaluator(doAssert=True))(node, environment)
        return Type.list(list)
