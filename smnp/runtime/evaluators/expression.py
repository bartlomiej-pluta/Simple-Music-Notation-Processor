from smnp.ast.node.factor import NotOperator, Power, Loop
from smnp.ast.node.identifier import FunctionCall, Assignment
from smnp.ast.node.term import Product
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
        from smnp.runtime.evaluators.power import PowerEvaluator
        from smnp.runtime.evaluators.loop import LoopEvaluator
        from smnp.runtime.evaluators.assignment import AssignmentEvaluator
        from smnp.runtime.evaluators.product import ProductEvaluator

        result = Evaluator.oneOf(
            Evaluator.forNodes(FunctionCallEvaluator.evaluate, FunctionCall),
            Evaluator.forNodes(MinusEvaluator.evaluate, MinusOperator),
            Evaluator.forNodes(AccessEvaluator.evaluate, Access),
            Evaluator.forNodes(NotEvaluator.evaluate, NotOperator),
            Evaluator.forNodes(PowerEvaluator.evaluate, Power),
            Evaluator.forNodes(LoopEvaluator.evaluate, Loop),
            Evaluator.forNodes(AssignmentEvaluator.evaluate, Assignment),
            Evaluator.forNodes(ProductEvaluator.evaluate, Product),
            AtomEvaluator.evaluate
        )(node, environment)

        if doAssert and result.result and result.value.type == Type.VOID:
            raise RuntimeException(f"Expected expression", node.pos)

        return result


    return evaluateExpression
