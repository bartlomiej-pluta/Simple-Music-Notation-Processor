from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.program import Program
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluators.list import evaluateList
from smnp.runtime.tools import flatListNode


def evaluateFunctionDefinition(definition, environment):
    name = definition.name
    params = list([p for p in flatListNode(definition.parameters)])
    body = definition.body

    if not isinstance(definition.parent, Program):
        raise RuntimeException(f"Functions can be defined only on the top level of script", name.pos)

    for p in params:
        if not isinstance(p, IdentifierNode):
            raise RuntimeException("Parameter of function definition must be an identifier", p.pos, )

    if name.identifier in environment.customFunctions or name.identifier in environment.functions:
        raise RuntimeException(f"Function '{name.identifier}' already exists", name.pos)

    environment.customFunctions[name.identifier] = {
        'params': params,
        'body': flatListNode(body)
    }


def evaluateFunctionCall(functionCall, environment):
    functionName = functionCall.identifier.identifier
    arguments = evaluateList(functionCall.arguments, environment).value
    return environment.invokeFunction(functionName, arguments)


# def evaluateFunctionCall(functionCall, environment):
#     funcName = functionCall.identifier.identifier
#     arguments = evaluateList(functionCall.arguments, environment)
#     for name, function in environment.customFunctions.items():
#         if funcName == name:
#             if len(function['params']) != len(arguments):
#                 raise RuntimeException(functionCall.pos, f"Calling '{funcName}' requires {len(function['params'])} and {len(arguments)} was passed")
#             environment.scopes.append({ function['params'][i].identifier: v for i, v in enumerate(arguments) })
#             returnValue = None
#             for node in function['body']:
#                 if not isinstance(node, ReturnNode):
#                     evaluate(node, environment)
#                 else:
#                     returnValue = evaluateReturn(node, environment)
#             environment.scopes.pop(-1)
#             return returnValue
#     for name, definition in environment.functions.items():
#         if name == funcName:
#             return definition(arguments, environment)
#     raise RuntimeException(functionCall.pos, f"Function '{funcName}' does not exist")