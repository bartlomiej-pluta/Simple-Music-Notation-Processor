from smnp.ast.node.atom import StringLiteral, IntegerLiteral, NoteLiteral, BoolLiteral, TypeLiteral
from smnp.ast.node.identifier import FunctionCall
from smnp.ast.node.list import List
from smnp.ast.node.map import Map
from smnp.ast.node.unit import MinusOperator
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


def expressionEvaluator(doAssert=False):
    def evaluateExpression(node, environment):
            from smnp.runtime.evaluators.atom import StringEvaluator
            from smnp.runtime.evaluators.atom import TypeEvaluator
            from smnp.runtime.evaluators.atom import IntegerEvaluator
            from smnp.runtime.evaluators.atom import NoteEvaluator
            from smnp.runtime.evaluators.atom import BoolEvaluator

            from smnp.runtime.evaluators.function import FunctionCallEvaluator
            from smnp.runtime.evaluators.atom import ListEvaluator
            from smnp.runtime.evaluators.atom import MapEvaluator
            from smnp.runtime.evaluators.minus import MinusEvaluator
            result =  Evaluator.oneOf(
                Evaluator.forNodes(FunctionCallEvaluator.evaluate, FunctionCall),
                Evaluator.forNodes(StringEvaluator.evaluate, StringLiteral),
                Evaluator.forNodes(IntegerEvaluator.evaluate, IntegerLiteral),
                Evaluator.forNodes(NoteEvaluator.evaluate, NoteLiteral),
                Evaluator.forNodes(BoolEvaluator.evaluate, BoolLiteral),
                Evaluator.forNodes(TypeEvaluator.evaluate, TypeLiteral),
                Evaluator.forNodes(ListEvaluator.evaluate, List),
                Evaluator.forNodes(MapEvaluator.evaluate, Map),
                Evaluator.forNodes(MinusEvaluator.evaluate, MinusOperator)
                # Evaluator.forNodes(IdentifierEvaluator.evaluate, Identifier),
                # Evaluator.forNodes(ListEvaluator.evaluate, List),
                # Evaluator.forNodes(AccessEvaluator.evaluate, LeftAssociativeOperatorNode),
                # Evaluator.forNodes(AssignmentEvaluator.evaluate, AssignmentNode),
                # Evaluator.forNodes(AsteriskEvaluator.evaluate, AsteriskNode),
                # Evaluator.forNodes(MapEvaluator.evaluate, MapNode)
            )(node, environment)

            if doAssert and result.result and result.value.type == Type.VOID:
                raise RuntimeException(f"Expected expression", node.pos)

            return result

    return evaluateExpression

