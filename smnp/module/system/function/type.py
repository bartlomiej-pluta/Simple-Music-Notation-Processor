from smnp.library.model import Function
from smnp.library.signature import signature, allTypes
from smnp.type.model import Type

_signature = signature(allTypes())
def _function(env, obj):
    return Type.type(obj.type)


function = Function(_signature, _function, 'typeOf')