from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class RelationEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        left = expressionEvaluator(doAssert=True)(node.left, environment).value
        right = expressionEvaluator(doAssert=True)(node.right, environment).value

        if node.operator.value == "==":
            return cls.equalOperatorEvaluator(left, node.operator, right)

        if node.operator.value == "!=":
            return cls.notEqualOperatorEvaluator(left, node.operator, right)

        return cls.otherRelationOperatorsEvaluator(left, node.operator, right)

    @classmethod
    def equalOperatorEvaluator(cls, left, operator, right):
        return Type.bool(left.value == right.value)

    @classmethod
    def notEqualOperatorEvaluator(cls, left, operator, right):
        return Type.bool(left.value != right.value)

    @classmethod
    def otherRelationOperatorsEvaluator(cls, left, operator, right):
        if left.type == right.type == Type.INTEGER:
            if operator.value == ">":
                return Type.bool(left.value > right.value)

            if operator.value == ">=":
                return Type.bool(left.value >= right.value)

            if operator.value == "<":
                return Type.bool(left.value < right.value)

            if operator.value == "<=":
                return Type.bool(left.value < right.value)

        raise RuntimeException(f"Operator {operator.value} is not supported by {left.type.name.lower()} and {right.type.name.lower()} types", operator.pos)

