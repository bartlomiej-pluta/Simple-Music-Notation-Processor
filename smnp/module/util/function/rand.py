import random as r

from smnp.error.function import IllegalArgumentException
from smnp.library.model import Function, CombinedFunction
from smnp.library.signature import varargSignature, listMatches, ofTypes
from smnp.type.model import Type


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