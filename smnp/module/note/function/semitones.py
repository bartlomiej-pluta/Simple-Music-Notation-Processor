from smnp.library.model import Function, CombinedFunction
from smnp.library.signature import varargSignature, ofTypes, listOf
from smnp.note.model import Note
from smnp.type.model import Type


_signature1 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))
def _function1(env, vararg):
    withoutPauses = [note.value for note in vararg if note.type == Type.NOTE]
    if len(withoutPauses) < 2:
        return Type.list([])
    return Type.list([Type.integer(Note.checkInterval(withoutPauses[i-1], withoutPauses[i])) for i in range(1, len(withoutPauses))]).decompose()


_signature2 = varargSignature(listOf(Type.NOTE, Type.INTEGER))
def _function2(env, vararg):
    return Type.list([_function1(env, arg.value) for arg in vararg]).decompose()


function = CombinedFunction(
    "semitones",
    Function(_signature1, _function1),
    Function(_signature2, _function2),
)