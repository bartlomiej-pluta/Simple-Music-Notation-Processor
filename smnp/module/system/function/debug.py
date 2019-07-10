from smnp.error.function import IllegalArgumentException
from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature = signature(ofTypes(Type.STRING))
def _function(env, parameter):
    if parameter.value == "environment":
        print(env)
        return
    elif parameter.value == "variables":
        print(env.scopesToString())
        return
    elif parameter.value == "functions":
        print(env.functionsToString())
        return
    elif parameter.value == "methods":
        print(env.methodsToString())
        return
    elif parameter.value == "callstack":
        print(env.callStackToString())
        return

    raise IllegalArgumentException(f"Unknown parameter '{parameter.value}'")


function = Function(_signature, _function, 'debug')