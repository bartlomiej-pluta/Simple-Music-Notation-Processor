import time

from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature = signature(ofTypes(Type.INTEGER))
def _function(env, value):
    time.sleep(value.value)


function = Function(_signature, _function, 'sleep')