from smnp.library.model import Function, CombinedFunction
from smnp.library.signature import varargSignature, listMatches, ofTypes, allTypes, signature, listOfMatchers
from smnp.type.model import Type

_signature1 = varargSignature(listMatches(ofTypes(Type.INTEGER, Type.STRING, Type.NOTE), allTypes()))
def _function1(env, vararg):
    map = {}
    for entry in vararg:
        key, value = entry.value
        map[key] = value

    return Type.map(map)


_signature2 = signature(listOfMatchers(listMatches(ofTypes(Type.INTEGER, Type.STRING, Type.NOTE), allTypes())))
def _function2(env, list):
    map = {}
    for entry in list.value:
        key, value = entry.value
        map[key] = value

    return Type.map(map)


function = CombinedFunction(
    'Map',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)