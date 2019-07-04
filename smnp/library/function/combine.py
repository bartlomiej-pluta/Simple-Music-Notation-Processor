from functools import reduce

from smnp.library.model import Function
from smnp.library.signature import varargSignature, ofTypes
from smnp.type.model import Type
from smnp.type.value import Value


def _combine(env, vararg):
    if len(vararg) == 1:
        return vararg[0]

    combined = reduce(lambda x, y: x.value + y.value, vararg)
    return Value(Type.LIST, combined)



_sign = varargSignature(ofTypes(Type.LIST))


combine = Function(_sign, _combine, 'combine')

