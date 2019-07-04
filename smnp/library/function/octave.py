from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type
from smnp.type.value import Value


def _withOctave(env, note, octave):
    return Value(Type.NOTE, note.value.withOctave(octave.value))


_sign = signature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER))


withOctave = Function(_sign, _withOctave, 'withOctave')