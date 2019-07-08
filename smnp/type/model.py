from enum import Enum

from smnp.error.runtime import RuntimeException
from smnp.note.model import Note
from smnp.type.value import Value


class Type(Enum):
    INTEGER = (int, lambda x: str(x))
    STRING = (str, lambda x: x)
    LIST = (list, lambda x: f"[{', '.join([e.stringify() for e in x])}]")
    PERCENT = (float, lambda x: f"{int(x * 100)}%")
    NOTE = (Note, lambda x: x.note.name)
    TYPE = (None, lambda x: str(x.type.name.lower()))
    VOID = (type(None), lambda x: _failStringify(Type.VOID))

    def stringify(self, element):
        return self.value[1](element)

    @staticmethod
    def integer(value):
        return Value(Type.INTEGER, value, {})

    @staticmethod
    def string(value):
        return Value(Type.STRING, value, {
            "length": Type.integer(len(value))
        })

    @staticmethod
    def list(value):
        return Value(Type.LIST, value, {
            "size": Type.integer(len(value))
        })

    @staticmethod
    def note(value):
        return Value(Type.NOTE, value, {
            "octave": Type.integer(value.octave),
            "duration": Type.integer(value.duration),
            "dot": Type.string('.' if value.dot else '')
        })

    @staticmethod
    def type(value):
        return Value(Type.TYPE, value, {})

    @staticmethod
    def void():
        return Value(Type.VOID, None)

def _failStringify(t):
    raise RuntimeException(f"Not able to interpret {t.name}'", None)



