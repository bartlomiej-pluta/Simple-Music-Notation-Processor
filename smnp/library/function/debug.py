from smnp.error.function import IllegalArgumentException
from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type

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

    raise IllegalArgumentException(f"Unknown parameter '{parameter.value}'")


function = Function(_signature, _function, 'debug')