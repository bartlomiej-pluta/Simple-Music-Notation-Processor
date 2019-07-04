import sys

from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type

_signature = signature(ofTypes(Type.INTEGER))
def _function(env, code):
    sys.exit(code.value)


function = Function(_signature, _function, 'exit')