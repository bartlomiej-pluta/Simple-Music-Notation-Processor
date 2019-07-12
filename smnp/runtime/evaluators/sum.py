from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class SumEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        left = expressionEvaluator(doAssert=True)(node.left, environment).value
        right = expressionEvaluator(doAssert=True)(node.right, environment).value

        if left.type == right.type == Type.INTEGER:
            return cls.integerEvaluator(left, node.operator, right)

        if left.type == right.type == Type.STRING:
            return cls.stringEvaluator(left, node.operator, right)

        if left.type == right.type == Type.LIST:
            return cls.listEvaluator(left, node.operator, right)

        if left.type == right.type == Type.MAP:
            return cls.mapEvaluator(left, node.operator, right)

        raise RuntimeException(f"Operator {node.operator.value} is not supported by {left.type.name.lower()} and {right.type.name.lower()} types", node.operator.pos)

    @classmethod
    def integerEvaluator(cls, left, operator, right):
        if operator.value == "+":
            return Type.integer(left.value + right.value)

        if operator.value == "-":
            return Type.integer(left.value - right.value)

        raise RuntimeError("This line should never be reached")

    @classmethod
    def stringEvaluator(cls, left, operator, right):
        if operator.value == "+":
            return Type.string(left.value + right.value)

        if operator.value == "-":
            raise RuntimeException(f"Operator {operator.value} is not supported by string types", operator.pos)

        raise RuntimeError("This line should never be reached")

    @classmethod
    def listEvaluator(cls, left, operator, right):
        if operator.value == "+":
            return Type.list(left.value + right.value)

        if operator.value == "-":
            raise RuntimeException(f"Operator {operator.value} is not supported by list types", operator.pos)

        raise RuntimeError("This line should never be reached")

    @classmethod
    def mapEvaluator(cls, left, operator, right):
        if operator.value == "+":
            return Type.map({**left.value, **right.value})

        if operator.value == "-":
            raise RuntimeException(f"Operator {operator.value} is not supported by map types", operator.pos)

        raise RuntimeError("This line should never be reached")