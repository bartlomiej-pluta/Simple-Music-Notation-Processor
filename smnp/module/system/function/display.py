from smnp.library.model import Function
from smnp.library.signature import varargSignature
from smnp.type.signature.matcher.type import allTypes

_signature = varargSignature(allTypes())
def _function(env, vararg):
    print("".join([arg.stringify() for arg in vararg]))


function = Function(_signature, _function, 'print')