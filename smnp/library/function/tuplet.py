from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import signature, listOf, ofTypes, varargSignature
from smnp.type.model import Type
from smnp.type.value import Value


_signature1 = varargSignature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER), ofTypes(Type.INTEGER))
def _function1(env, n, m, vararg):
    t = [Value(Type.NOTE, arg.value.withDuration(arg.value.duration * n.value / m.value)) for arg in vararg]
    return Value(Type.LIST, t).decompose()



_signature2 = signature(ofTypes(Type.INTEGER), ofTypes(Type.INTEGER), listOf(Type.NOTE))
def _function2(env, n, m, notes):
    return _function1(env, n, m, notes.value)


function = CombinedFunction(
    'tuplet',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)
