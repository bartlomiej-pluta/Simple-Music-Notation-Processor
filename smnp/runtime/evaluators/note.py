from smnp.type.model import Type
from smnp.type.value import Value


def evaluateNote(note, environment):
    return Value(Type.NOTE, note.value)