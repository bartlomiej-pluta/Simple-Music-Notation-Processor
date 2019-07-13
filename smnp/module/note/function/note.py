from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.note.model import Note
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = signature(ofType(Type.STRING), ofType(Type.INTEGER), ofType(Type.INTEGER), ofType(Type.BOOL))
def _function(env, note, octave, duration, dot):
    return Type.note(Note(note.value, octave.value, duration.value, dot.value))

function = Function(_signature, _function, 'Note')