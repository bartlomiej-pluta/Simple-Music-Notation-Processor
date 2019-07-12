from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class NotEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        value = expressionEvaluator(doAssert=True)(node.value, environment).value

        if value.type != Type.BOOL:
            raise RuntimeException(f"Operator '{node.operator.value}' is supported only by {Type.BOOL.name.lower()} type", node.pos)

        return Type.bool(not value.value)