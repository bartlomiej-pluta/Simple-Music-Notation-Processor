from smnp.library.model import Function
from smnp.library.signature import varargSignature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = varargSignature(ofType(Type.STRING))
def _function(env, vararg):
    return Type.string("".join([ arg.value for arg in vararg ]))


function = Function(_signature, _function, 'concat')