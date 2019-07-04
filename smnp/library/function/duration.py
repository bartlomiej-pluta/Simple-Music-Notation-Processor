from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type
from smnp.type.value import Value


def _withDuration(env, note, duration):
    return Value(Type.NOTE, note.value.withDuration(duration.value))


_sign = signature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER))


withDuration = Function(_sign, _withDuration, 'withDuration')