from smnp.library.model import Function, CombinedFunction
from smnp.library.signature import varargSignature, ofTypes, listOf
from smnp.note.model import Note
from smnp.type.model import Type
from smnp.type.value import Value


def _semitones1(env, vararg):
    withoutPauses = [note.value for note in vararg if note.type == Type.NOTE]
    if len(withoutPauses) < 2:
        return Value(Type.LIST, [])
    return Value(Type.LIST, [Value(Type.INTEGER, Note.checkInterval(withoutPauses[i-1], withoutPauses[i])) for i in range(1, len(withoutPauses))]).decompose()


_sign1 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))


def _semitones2(env, vararg):
    return Value(Type.LIST, [_semitones1(env, arg.value) for arg in vararg]).decompose()


_sign2 = varargSignature(listOf(Type.NOTE, Type.INTEGER))


semitones = CombinedFunction(
    "semitones",
    Function(_sign1, _semitones1),
    Function(_sign2, _semitones2),
)