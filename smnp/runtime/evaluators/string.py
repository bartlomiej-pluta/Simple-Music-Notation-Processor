import re

from smnp.error.runtime import RuntimeException
from smnp.type.model import Type
from smnp.type.value import Value


def evaluateString(string, environment):
    value = interpolate(string, environment)
    return Value(Type.STRING, value)


def interpolate(string, environment):
    interpolated = string.value
    for scope in reversed(environment.scopes):
        for name, value in scope.items():
            interpolated = interpolated.replace('{' + name + '}', value.stringify())

    nonMatchedVariables = re.findall(r"\{\w+\}", interpolated)
    if len(nonMatchedVariables) > 0:
        raise RuntimeException(f"Variable '{nonMatchedVariables[0][1:len(nonMatchedVariables[0])-1]}' is not declared",
                               (string.pos[0], string.pos[1] + string.value.find(nonMatchedVariables[0])+1))

    return interpolated

# or scope in reversed(environment.scopes):
#         for k, v in scope.items():
#             value = value.replace('{' + k + '}', v) #TODO: poprawic