import time

from smnp.library.model import Function
from smnp.library.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature = signature(ofTypes(Type.INTEGER))
def _function(env, value):
    time.sleep(value.value)


function = Function(_signature, _function, 'sleep')