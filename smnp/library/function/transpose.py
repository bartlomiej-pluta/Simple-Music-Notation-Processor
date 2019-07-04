from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import varargSignature, ofTypes, listOf
from smnp.type.model import Type
from smnp.type.value import Value


def _transpose1(env, value, vararg):
    transposed = [Value(Type.NOTE, arg.value.transpose(value.value)) if arg.type == Type.NOTE else arg for arg in vararg]
    return Value(Type.LIST, transposed).decompose()


_sign1 = varargSignature(ofTypes(Type.INTEGER, Type.NOTE), ofTypes(Type.INTEGER))


def _transpose2(env, value, vararg):
    return Value(Type.LIST, [_transpose1(env, value, arg.value) for arg in vararg]).decompose()


_sign2 = varargSignature(listOf(Type.INTEGER, Type.NOTE), ofTypes(Type.INTEGER))


transpose = CombinedFunction(
    'transpose',
    Function(_sign1, _transpose1),
    Function(_sign2, _transpose2)
)
