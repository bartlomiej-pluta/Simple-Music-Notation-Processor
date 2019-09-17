from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class PowerEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        left = expressionEvaluator(doAssert=True)(node.left, environment).value
        right = expressionEvaluator(doAssert=True)(node.right, environment).value
        supportedTypes = [Type.INTEGER, Type.FLOAT]

        if not left.type in supportedTypes:
            raise RuntimeException(f"Operator '{node.operator.value}' is supported only by {Type.INTEGER.name.lower()} type", node.left.pos)

        if not right.type in supportedTypes:
            raise RuntimeException(f"Operator '{node.operator.value}' is supported only by {[t.name.lower() for t in supportedTypes]} type", node.right.pos)

        return Type.float(float(left.value ** right.value))