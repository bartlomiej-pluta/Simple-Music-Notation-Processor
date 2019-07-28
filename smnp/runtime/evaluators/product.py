from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class ProductEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        left = expressionEvaluator(doAssert=True)(node.left, environment).value
        right = expressionEvaluator(doAssert=True)(node.right, environment).value
        supportedTypes = [Type.INTEGER, Type.FLOAT]

        if not left.type in supportedTypes:
            raise RuntimeException(
                f"Operator '{node.operator.value}' is supported only by {[t.name.lower() for t in supportedTypes]} type", node.left.pos)

        if not right.type in supportedTypes:
            raise RuntimeException(
                f"Operator '{node.operator.value}' is supported only by {[t.name.lower() for t in supportedTypes]} type", node.right.pos)

        if node.operator.value == "*":
            return getProperTypeProvider(left.value * right.value)

        if node.operator.value == "/":
            if right.value == 0:
                raise RuntimeException("Attempt to divide by 0", node.right.pos)

            value = left.value / right.value

            if left.type == right.type == Type.INTEGER and int(value) == value:
                return Type.integer(int(value))

            return getProperTypeProvider(value)

        raise RuntimeError("This line should never be reached")


def getProperTypeProvider(value):
    return {
        int: lambda v: Type.integer(v),
        float: lambda v: Type.float(v)
    }[type(value)](value)

