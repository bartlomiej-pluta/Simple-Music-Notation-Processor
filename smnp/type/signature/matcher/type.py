from smnp.type.model import Type
from smnp.type.signature.matcher.model import Matcher


def allTypes():
    allowedTypes = [t for t in Type if t != Type.VOID]
    return ofTypes(*allowedTypes)


def ofTypes(*types):
    def check(value):
        return value.type in types
    return Matcher(None, check, f"<{', '.join([t.name.lower() for t in types])}>")


def ofType(type):
    def check(value):
        return value.type == type

    return Matcher(None, check, type.name.lower())