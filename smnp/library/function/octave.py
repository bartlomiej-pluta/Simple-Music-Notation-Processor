from smnp.library.model import Function
from smnp.library.signature import signature, ofType
from smnp.type.model import Type

_signature = signature(ofType(Type.NOTE), ofType(Type.INTEGER))
def _function(env, note, octave):
    return Type.note(note.value.withOctave(octave.value))


function = Function(_signature, _function, 'withOctave')