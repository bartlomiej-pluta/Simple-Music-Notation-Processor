from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import evaluate
from smnp.type.model import Type


def evaluateAssignment(assignment, environment):
    target = assignment.target.identifier
    value = evaluate(assignment.value, environment)
    if value.type == Type.VOID:
        raise RuntimeException(f"Expected expression, found '{value.type.name}'", assignment.value.pos)
    scopeOfExistingVariable = environment.findVariableScope(target)
    if scopeOfExistingVariable is not None:
        scopeOfExistingVariable[target] = value
    else:
        environment.scopes[-1][target] = value