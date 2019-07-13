import random

from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = signature(ofType(Type.INTEGER), ofType(Type.INTEGER))
def _function(env, min, max):
    return Type.integer(random.randint(min.value, max.value))

function = Function(_signature, _function, 'rand')