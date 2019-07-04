from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import varargSignature, ofTypes, listOf
from smnp.type.model import Type
from smnp.type.value import Value


_signature1 = varargSignature(ofTypes(Type.INTEGER, Type.NOTE), ofTypes(Type.INTEGER))
def _function1(env, value, vararg):
    transposed = [Value(Type.NOTE, arg.value.transpose(value.value)) if arg.type == Type.NOTE else arg for arg in vararg]
    return Value(Type.LIST, transposed).decompose()


_signature2 = varargSignature(listOf(Type.INTEGER, Type.NOTE), ofTypes(Type.INTEGER))
def _function2(env, value, vararg):
    return Value(Type.LIST, [_function1(env, value, arg.value) for arg in vararg]).decompose()


function = CombinedFunction(
    'transpose',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)
