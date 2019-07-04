from enum import Enum

from smnp.error.runtime import RuntimeException
from smnp.note.model import Note


class Type(Enum):
    INTEGER = (int, lambda x: str(x))
    STRING = (str, lambda x: x)
    LIST = (list, lambda x: f"({', '.join([e.stringify() for e in x])})")
    PERCENT = (float, lambda x: f"{int(x * 100)}%")
    NOTE = (Note, lambda x: x.note.name)
    VOID = (type(None), lambda x: _failStringify(Type.VOID))

    def stringify(self, element):
        return self.value[1](element)


def _failStringify(t):
    raise RuntimeException(f"Not able to interpret {t.name}'")



