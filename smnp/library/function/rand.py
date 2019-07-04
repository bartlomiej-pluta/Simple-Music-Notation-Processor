import random as r

from smnp.error.function import IllegalArgumentException
from smnp.library.model import Function, CombinedFunction
from smnp.library.signature import varargSignature, listMatches, ofTypes
from smnp.type.model import Type


def forType(t):
    def _random(env, vararg):
        choice = r.random()
        acc = 0
        if sum(arg.value[0].value for arg in vararg) != 1.0:
            raise IllegalArgumentException("Sum of all percentage values must be equal 100%")
        for arg in vararg:
            percent, item = arg.value
            acc += percent.value
            if choice <= acc:
                return item

    _sign = varargSignature(listMatches(ofTypes(Type.PERCENT), ofTypes(t)))

    return Function(_sign, _random)


random = CombinedFunction('random', *[ forType(t) for t in Type if t != Type.VOID ])
#
# def random(args, env):
#     if not all(isinstance(x, list) and len(x) == 2 and isinstance(x[0], float) for x in args):
#         return # not valid signature
#     if sum([x[0] for x in args]) != 1.0:
#         return # not sums to 100%
#     choice = r.random()
#     acc = 0
#     for e in args:
#         acc += e[0]
#         if choice <= acc:
#             return e[1]
#

#TODO: sample