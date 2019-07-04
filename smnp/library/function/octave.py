from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type
from smnp.type.value import Value


_signature = signature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER))
def _function(env, note, octave):
    return Value(Type.NOTE, note.value.withOctave(octave.value))


function = Function(_signature, _function, 'withOctave')