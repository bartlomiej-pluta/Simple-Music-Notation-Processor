from smnp.ast.node.access import AccessNode
from smnp.ast.node.assignment import AssignmentNode
from smnp.ast.node.asterisk import AsteriskNode
from smnp.ast.node.block import BlockNode
from smnp.ast.node.colon import ColonNode
from smnp.ast.node.function import FunctionDefinitionNode, FunctionCallNode
from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.node.list import ListNode
from smnp.ast.node.note import NoteLiteralNode
from smnp.ast.node.percent import PercentNode
from smnp.ast.node.program import Program
from smnp.ast.node.string import StringLiteralNode

def evaluate(input, environment):
    from smnp.runtime.evaluators.access import evaluateAccess
    from smnp.runtime.evaluators.assignment import evaluateAssignment
    from smnp.runtime.evaluators.asterisk import evaluateAsterisk
    from smnp.runtime.evaluators.block import evaluateBlock
    from smnp.runtime.evaluators.colon import evaluateColon
    from smnp.runtime.evaluators.function import evaluateFunctionDefinition, evaluateFunctionCall
    from smnp.runtime.evaluators.identifier import evaluateIdentifier
    from smnp.runtime.evaluators.integer import evaluateInteger
    from smnp.runtime.evaluators.list import evaluateList
    from smnp.runtime.evaluators.note import evaluateNote
    from smnp.runtime.evaluators.percent import evaluatePercent
    from smnp.runtime.evaluators.program import evaluateProgram
    from smnp.runtime.evaluators.string import evaluateString

    if isinstance(input, Program):
        return evaluateProgram(input, environment)
    if isinstance(input, IntegerLiteralNode):
        return evaluateInteger(input, environment)
    if isinstance(input, PercentNode):
        return evaluatePercent(input, environment)
    if isinstance(input, StringLiteralNode):
        return evaluateString(input, environment)
    if isinstance(input, NoteLiteralNode):
        return evaluateNote(input, environment)
    if isinstance(input, FunctionDefinitionNode):
        return evaluateFunctionDefinition(input, environment)
    if isinstance(input, FunctionCallNode):
        return evaluateFunctionCall(input, environment)
    if isinstance(input, AccessNode):
        return evaluateAccess(input, environment)
    if isinstance(input, BlockNode):
        return evaluateBlock(input, environment)
    if isinstance(input, ListNode):
        return evaluateList(input, environment)
    if isinstance(input, AssignmentNode):
        return evaluateAssignment(input, environment)
    if isinstance(input, AsteriskNode):
        return evaluateAsterisk(input, environment)
    if isinstance(input, ColonNode):
        return evaluateColon(input, environment)
    if isinstance(input, IdentifierNode):
        return evaluateIdentifier(input, environment)