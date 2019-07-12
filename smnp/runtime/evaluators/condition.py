from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class IfElseEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        condition = expressionEvaluator(doAssert=True)(node.condition, environment).value

        if condition.type != Type.BOOL:
            raise RuntimeException(f"Only {Type.BOOL.name.lower()} types can be used as conditions in conditional expression", node.condition.pos)

        if condition.value:
            return expressionEvaluator(doAssert=True)(node.ifNode, environment).value
        else:
            return expressionEvaluator(doAssert=True)(node.elseNode, environment).value


class IfElseStatementEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        condition = expressionEvaluator(doAssert=True)(node.condition, environment).value

        if condition.type != Type.BOOL:
            raise RuntimeException(
                f"Only {Type.BOOL.name.lower()} types can be used as conditions in conditional expression", node.condition.pos)

        if condition.value:
            evaluate(node.ifNode, environment)
        else:
            evaluate(node.elseNode, environment)