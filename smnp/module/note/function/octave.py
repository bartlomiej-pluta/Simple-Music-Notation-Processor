from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = signature(ofType(Type.NOTE), ofType(Type.INTEGER))
def _function(env, note, octave):
    return Type.note(note.value.withOctave(octave.value))


function = Function(_signature, _function, 'withOctave')