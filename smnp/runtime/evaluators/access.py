from smnp.ast.node.access import AccessNode
from smnp.ast.node.function import FunctionCallNode
from smnp.error.base import SmnpException
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import evaluate
from smnp.runtime.evaluators.list import evaluateList


def evaluateAccess(access, environment):
    element = evaluate(access.element, environment)
    if type(access.property) == FunctionCallNode:
        return evaluateMethodCall(element, access.property, environment)
    if type(access.property) == AccessNode:
        return evaluateAccess(access.property, environment)

    raise RuntimeException("Not implemented yet", access.property.pos)
    # TODO only methods can be handled so far


def evaluateMethodCall(element, methodCall, environment):
    try:
        methodName = methodCall.identifier.identifier
        arguments = evaluateList(methodCall.arguments, environment)

        return environment.invokeMethod(methodName, element, arguments)

    except SmnpException as e:
        e.pos = methodCall.pos
        raise e
# for name, library in environment.customFunctions.items():
# if funcName == name:
# if len(library['params']) != len(arguments):
# raise RuntimeException(functionCall.pos, f"Calling '{funcName}' requires {len(library['params'])} and {len(arguments)} was passed")
# environment.scopes.append({ library['params'][i].identifier: v for i, v in enumerate(arguments) })
# returnValue = None
# for node in library['body']:
# if not isinstance(node, ReturnNode):
# evaluate(node, environment)
# else:
# returnValue = evaluateReturn(node, environment)
# environment.scopes.pop(-1)
# return returnValue
