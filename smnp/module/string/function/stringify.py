from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import allTypes

_signature = signature(allTypes())
def _function(env, object):
    return Type.string(object.stringify())

function = Function(_signature, _function, 'toString')