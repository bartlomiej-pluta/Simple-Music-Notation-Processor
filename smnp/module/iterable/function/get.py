from smnp.error.runtime import RuntimeException
from smnp.function.model import CombinedFunction, Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes, ofType

_signature1 = signature(ofType(Type.LIST), ofType(Type.INTEGER))
def _function1(env, list, index):
    try:
        return list.value[index.value]
    except IndexError:
        raise RuntimeException(f"Attempt to access item which is outside the list", None)


_signature2 = signature(ofType(Type.MAP), ofTypes(Type.INTEGER, Type.STRING, Type.NOTE, Type.BOOL, Type.TYPE))
def _function2(env, map, key):
    try:
        return map.value[key]
    except KeyError:
        raise RuntimeException(f"Attempt to access unknown key in map", None)


function = CombinedFunction(
    'get',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)