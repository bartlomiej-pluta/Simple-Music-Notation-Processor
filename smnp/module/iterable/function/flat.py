from smnp.function.model import Function
from smnp.function.signature import varargSignature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import allTypes

_signature = varargSignature(allTypes())
def _function(env, vararg):
    return Type.list(doFlat(vararg, [])).decompose()


def doFlat(input, output=None):
    if output is None:
        output = []

    for item in input:
        if item.type == Type.LIST:
            doFlat(item.value, output)
        else:
            output.append(item)
    return output


function = Function(_signature, _function, 'flat')