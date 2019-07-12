from smnp.ast.node.identifier import Identifier, FunctionCall
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools.error import updatePos


class UnitEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return


class AccessEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        left = expressionEvaluator(doAssert=True)(node.left, environment).value  # TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
        right = node.right

        if type(right) == Identifier:
            try:
                return left.properties[right.value]
            except KeyError:
                raise RuntimeException(f"Unknown property '{right.value}' of type '{left.type.name.lower()}'", right.pos)

        if type(right) == FunctionCall:
            try:
                arguments = abstractIterableEvaluator(expressionEvaluator(doAssert=True))(right.arguments, environment)
                return environment.invokeMethod(left, right.name.value, arguments)
            except RuntimeException as e:
                raise updatePos(e, right)