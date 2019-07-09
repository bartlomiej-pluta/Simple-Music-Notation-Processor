from smnp.function.model import CombinedFunction, Function
from smnp.function.signature import signature, varargSignature
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf
from smnp.type.signature.matcher.type import ofTypes

_signature1 = varargSignature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER), ofTypes(Type.INTEGER))
def _function1(env, n, m, vararg):
    t = [Type.note(arg.value.withDuration(int(arg.value.duration * n.value / m.value))) for arg in vararg]
    return Type.list(t).decompose()



_signature2 = signature(ofTypes(Type.INTEGER), ofTypes(Type.INTEGER), listOf(Type.NOTE))
def _function2(env, n, m, notes):
    return _function1(env, n, m, notes.value)


function = CombinedFunction(
    'tuplet',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)
