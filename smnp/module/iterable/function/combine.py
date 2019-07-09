from functools import reduce

from smnp.function.model import Function
from smnp.function.signature import varargSignature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature = varargSignature(ofTypes(Type.LIST))
def _function(env, vararg):
    if len(vararg) == 1:
        return vararg[0]

    combined = reduce(lambda x, y: x.value + y.value, vararg)
    return Type.list(combined)


function = Function(_signature, _function, 'combine')

