from smnp.library.model import Function
from smnp.library.signature import varargSignature, allTypes
from smnp.type.model import Type
from smnp.type.value import Value


def _flat(env, vararg):
    return Value(Type.LIST, doFlat(vararg, [])).decompose()

def doFlat(input, output=[]):
    for item in input:
        if item.type == Type.LIST:
            doFlat(item.value, output)
        else:
            output.append(item)
    return output


_sign = varargSignature(allTypes())

flat = Function(_sign, _flat, 'flat')