from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.type.model import Type


class MinusEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        value = evaluate(node.value, environment).value
        try:
            return {
                Type.INTEGER: cls.evaluateForInteger,
                Type.FLOAT: cls.evaluateForFloat,
                Type.STRING: cls.evaluateForString,
                Type.LIST: cls.evaluateForList
            }[value.type](value.value)
        except KeyError:
            raise RuntimeException(f"Type {value.type.name.lower()} does not support '{node.operator.value}' operator", node.pos)

    @classmethod
    def evaluateForInteger(cls, value):
        return Type.integer(-value)

    @classmethod
    def evaluateForFloat(cls, value):
        return Type.float(-value)

    @classmethod
    def evaluateForString(cls, value):
        return Type.string(value[::-1])

    @classmethod
    def evaluateForList(cls, value):
        return Type.list(value[::-1])