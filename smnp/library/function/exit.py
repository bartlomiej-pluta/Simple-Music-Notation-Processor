import sys

from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type


def _exit(env, code):
    sys.exit(code.value)

_sign = signature(ofTypes(Type.INTEGER))

exit = Function(_sign, _exit, 'exit')