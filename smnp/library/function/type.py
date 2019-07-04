from smnp.library.model import Function
from smnp.library.signature import signature, allTypes


_signature = signature(allTypes())
def _function(env, obj):
    return obj.type.name


function = Function(_signature, _function, 'type')