from smnp.function.model import CombinedFunction, Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature1 = signature(ofType(Type.INTEGER))
def _function1(env, value):
    return Type.float(float(value.value))


_signature2 = signature(ofType(Type.STRING))
def _function2(env, value):
    return Type.float(float(value.value))


_signature3 = signature(ofType(Type.FLOAT))
def _function3(env, value):
    return value


function = CombinedFunction(
    'Float',
    Function(_signature1, _function1),
    Function(_signature2, _function2),
    Function(_signature3, _function3),
)