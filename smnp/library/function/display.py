from smnp.library.model import Function
from smnp.library.signature import varargSignature, allTypes


_signature = varargSignature(allTypes())
def _function(env, vararg):
    print("".join([arg.stringify() for arg in vararg]))


function = Function(_signature, _function, 'print')