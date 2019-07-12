from smnp.ast.node.factor import NotOperator
from smnp.ast.node.identifier import FunctionCall
from smnp.ast.node.unit import MinusOperator, Access
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


def expressionEvaluator(doAssert=False):
    def evaluateExpression(node, environment):
        from smnp.runtime.evaluators.function import FunctionCallEvaluator
        from smnp.runtime.evaluators.minus import MinusEvaluator

        from smnp.runtime.evaluators.atom import AtomEvaluator
        from smnp.runtime.evaluators.access import AccessEvaluator
        from smnp.runtime.evaluators.negation import NotEvaluator
        result = Evaluator.oneOf(
            Evaluator.forNodes(FunctionCallEvaluator.evaluate, FunctionCall),
            Evaluator.forNodes(MinusEvaluator.evaluate, MinusOperator),
            Evaluator.forNodes(AccessEvaluator.evaluate, Access),
            Evaluator.forNodes(NotEvaluator.evaluate, NotOperator),
            AtomEvaluator.evaluate
        )(node, environment)

        if doAssert and result.result and result.value.type == Type.VOID:
            raise RuntimeException(f"Expected expression", node.pos)

        return result


    return evaluateExpression
