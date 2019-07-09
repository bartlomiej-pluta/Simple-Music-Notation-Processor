import random as r

from smnp.error.function import IllegalArgumentException
from smnp.function.model import Function, CombinedFunction
from smnp.function.signature import varargSignature
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listMatches
from smnp.type.signature.matcher.type import ofTypes


def forType(t):
    _signature = varargSignature(listMatches(ofTypes(Type.PERCENT), ofTypes(t)))
    def _function(env, vararg):
        choice = r.random()
        acc = 0
        if sum(arg.value[0].value for arg in vararg) != 1.0:
            raise IllegalArgumentException("Sum of all percentage values must be equal 100%")
        for arg in vararg:
            percent, item = arg.value
            acc += percent.value
            if choice <= acc:
                return item

    return Function(_signature, _function)


function = CombinedFunction('random', *[ forType(t) for t in Type if t != Type.VOID ])

#TODO: sample