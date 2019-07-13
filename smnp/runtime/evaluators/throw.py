from smnp.error.custom import CustomException
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class ThrowEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        string = expressionEvaluator(doAssert=True)(node.value, environment).value

        if string.type != Type.STRING:
            raise RuntimeException(f"Only {Type.STRING.name.lower()} types can be thrown", node.value.pos)

        raise CustomException(string.value, node.pos)