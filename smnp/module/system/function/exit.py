import sys

from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature = signature(ofTypes(Type.INTEGER))
def _function(env, code):
    sys.exit(code.value)


function = Function(_signature, _function, 'exit')