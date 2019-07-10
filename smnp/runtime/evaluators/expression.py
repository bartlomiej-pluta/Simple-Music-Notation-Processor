from smnp.ast.node.access import LeftAssociativeOperatorNode
from smnp.ast.node.assignment import AssignmentNode
from smnp.ast.node.asterisk import AsteriskNode
from smnp.ast.node.bool import BoolLiteralNode
from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.node.invocation import FunctionCallNode
from smnp.ast.node.list import ListNode
from smnp.ast.node.map import MapNode
from smnp.ast.node.note import NoteLiteralNode
from smnp.ast.node.string import StringLiteralNode
from smnp.ast.node.type import TypeNode
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


def expressionEvaluator(doAssert=False):
    def evaluateExpression(node, environment):
            from smnp.runtime.evaluators.string import StringEvaluator
            from smnp.runtime.evaluators.integer import IntegerEvaluator
            from smnp.runtime.evaluators.note import NoteEvaluator
            from smnp.runtime.evaluators.identifier import IdentifierEvaluator
            from smnp.runtime.evaluators.list import ListEvaluator
            from smnp.runtime.evaluators.function import FunctionCallEvaluator

            from smnp.runtime.evaluators.access import AccessEvaluator
            from smnp.runtime.evaluators.assignment import AssignmentEvaluator
            from smnp.runtime.evaluators.asterisk import AsteriskEvaluator
            from smnp.runtime.evaluators.map import MapEvaluator
            from smnp.runtime.evaluators.type import TypeEvaluator
            from smnp.runtime.evaluators.bool import BoolEvaluator
            result =  Evaluator.oneOf(
                Evaluator.forNodes(FunctionCallEvaluator.evaluate, FunctionCallNode),
                Evaluator.forNodes(StringEvaluator.evaluate, StringLiteralNode),
                Evaluator.forNodes(IntegerEvaluator.evaluate, IntegerLiteralNode),
                Evaluator.forNodes(NoteEvaluator.evaluate, NoteLiteralNode),
                Evaluator.forNodes(BoolEvaluator.evaluate, BoolLiteralNode),
                Evaluator.forNodes(TypeEvaluator.evaluate, TypeNode),
                Evaluator.forNodes(IdentifierEvaluator.evaluate, IdentifierNode),
                Evaluator.forNodes(ListEvaluator.evaluate, ListNode),
                Evaluator.forNodes(AccessEvaluator.evaluate, LeftAssociativeOperatorNode),
                Evaluator.forNodes(AssignmentEvaluator.evaluate, AssignmentNode),
                Evaluator.forNodes(AsteriskEvaluator.evaluate, AsteriskNode),
                Evaluator.forNodes(MapEvaluator.evaluate, MapNode)
            )(node, environment)

            if doAssert and result.result and result.value.type == Type.VOID:
                raise RuntimeException(f"Expected expression", node.pos)

            return result

    return evaluateExpression

