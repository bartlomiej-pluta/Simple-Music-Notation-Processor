from enum import Enum

from smnp.audio.sound import Sound
from smnp.error.runtime import RuntimeException
from smnp.note.model import Note
from smnp.type.value import Value


class Type(Enum):
    INTEGER = (int, lambda x: str(x))
    FLOAT = (float, lambda x: str(x))
    STRING = (str, lambda x: x)
    LIST = (list, lambda x: f"[{', '.join([e.stringify() for e in x])}]")
    MAP = (dict, lambda x: '{' + ', '.join(f"'{k.stringify()}' -> '{v.stringify()}'" for k, v in x.items()) + '}')
    PERCENT = (float, lambda x: f"{int(x * 100)}%")
    NOTE = (Note, lambda x: x.note.name)
    BOOL = (bool, lambda x: str(x).lower())
    SOUND = (Sound, lambda x: x.file)
    TYPE = (None, lambda x: x.name.lower())
    VOID = (type(None), lambda x: _failStringify(Type.VOID))

    def stringify(self, element):
        return self.value[1](element)

    @staticmethod
    def integer(value):
        return Value(Type.INTEGER, value, {})

    @staticmethod
    def float(value):
        return Value(Type.FLOAT, value, {})

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
    def map(value):
        return Value(Type.MAP, value, {
            "size": Type.integer(len(value)),
            "keys": Type.list([ k for k, v in value.items() ]),
            "values": Type.list([ v for k, v in value.items() ])
        })

    @staticmethod
    def note(value):
        return Value(Type.NOTE, value, {
            "pitch": Type.string(str(value.note)),
            "octave": Type.integer(value.octave),
            "duration": Type.integer(value.duration),
            "dot": Type.bool(value.dot)
        })

    @staticmethod
    def bool(value):
        return Value(Type.BOOL, value, {})

    @staticmethod
    def sound(value):
        return Value(Type.SOUND, value, {
            "file": Type.string(value.file),
            "fs": Type.integer(value.fs)
        })

    @staticmethod
    def type(value):
        return Value(Type.TYPE, value, {})

    @staticmethod
    def void():
        return Value(Type.VOID, None)


def _failStringify(t):
    raise RuntimeException(f"Not able to interpret {t.name}'", None)



