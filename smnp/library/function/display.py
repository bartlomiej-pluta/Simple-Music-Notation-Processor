from smnp.library.model import Function
from smnp.library.signature import varargSignature, allTypes


def _display(env, vararg):
    print("".join([arg.stringify() for arg in vararg]))

_sign = varargSignature(allTypes())

display = Function(_sign, _display, 'print')