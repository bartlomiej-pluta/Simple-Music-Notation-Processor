from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.node.list import ListNode
from smnp.ast.node.note import NoteLiteralNode
from smnp.ast.node.string import StringLiteralNode
from smnp.runtime.evaluator import Evaluator


def evaluateExpression(node, environment):
        from smnp.runtime.evaluators.string import StringEvaluator
        from smnp.runtime.evaluators.integer import IntegerEvaluator
        from smnp.runtime.evaluators.note import NoteEvaluator
        from smnp.runtime.evaluators.identifier import IdentifierEvaluator
        from smnp.runtime.evaluators.list import ListEvaluator

        return Evaluator.oneOf(
            Evaluator.forNodes(StringEvaluator.evaluate, StringLiteralNode),
            Evaluator.forNodes(IntegerEvaluator.evaluate, IntegerLiteralNode),
            Evaluator.forNodes(NoteEvaluator.evaluate, NoteLiteralNode),
            Evaluator.forNodes(IdentifierEvaluator.evaluate, IdentifierNode),
            Evaluator.forNodes(ListEvaluator.evaluate, ListNode)
        )(node, environment)