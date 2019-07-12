from smnp.ast.node.identifier import Identifier, FunctionCall
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools.error import updatePos


class AccessEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        left = expressionEvaluator(doAssert=True)(node.left, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
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

#
# def evaluateAccess(access, environment):
#     element = evaluate(access.element, environment)
#     if type(access.property) == FunctionCallNode:
#         return evaluateMethodCall(element, access.property, environment)
#     if type(access.property) == AccessNode:
#         return evaluateAccess(access.property, environment)
#
#     raise RuntimeException("Not implemented yet", access.property.pos)
#     # TODO only methods can be handled so far
#
#
# def evaluateMethodCall(element, methodCall, environment):
#     try:
#         methodName = methodCall.identifier.identifier
#         arguments = evaluateList(methodCall.arguments, environment)
#
#         return environment.invokeMethod(methodName, element, arguments)
#
#     except SmnpException as e:
#         e.pos = methodCall.pos
#         raise e
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
