from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluators.list import evaluateList


def evaluateAccess(access, environment):
    pass
    #element = evaluate(access.element, environment)
    # TODO: narazie tylko metody działają
    #e = evaluateMethodCall(element, access.property, environment)



def evaluateMethodCall(element, functionCall, environment):
    funcName = functionCall.identifier.identifier
    arguments = evaluateList(functionCall.arguments, environment)
    arguments.insert(0, element)
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
    for name, definition in environment.methods[type(element)].items():
        if name == funcName:
            return definition(arguments, environment)
    raise RuntimeException(f"Method '{funcName}' does not exist", functionCall.pos)