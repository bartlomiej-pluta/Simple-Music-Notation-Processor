from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import varargSignature
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf
from smnp.type.signature.matcher.type import ofTypes

_signature1 = varargSignature(ofTypes(Type.INTEGER, Type.NOTE), ofTypes(Type.INTEGER))
def _function1(env, value, vararg):
    transposed = [Type.note(arg.value.transpose(value.value)) if arg.type == Type.NOTE else arg for arg in vararg]
    return Type.list(transposed).decompose()


_signature2 = varargSignature(listOf(Type.INTEGER, Type.NOTE), ofTypes(Type.INTEGER))
def _function2(env, value, vararg):
    return Type.list([_function1(env, value, arg.value) for arg in vararg]).decompose()


function = CombinedFunction(
    'transpose',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)
