from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator


class AssignmentEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        target = node.left.value
        value = expressionEvaluator(doAssert=True)(node.right, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
        scopeOfExistingVariable = environment.findVariableScope(target)
        if scopeOfExistingVariable is None:
            environment.scopes[-1][target] = value
        else:
            scopeOfExistingVariable[target] = value

        return value

#
# def evaluateAssignment(assignment, environment):
#     target = assignment.target.identifier
#     value = evaluate(assignment.value, environment)
#     if value.type == Type.VOID:
#         raise RuntimeException(f"Expected expression, found '{value.type.name}'", assignment.value.pos)
#     scopeOfExistingVariable = environment.findVariableScope(target)
#     if scopeOfExistingVariable is not None:
#         scopeOfExistingVariable[target] = value
#     else:
#         environment.scopes[-1][target] = value