from smnp.type.model import Type
from smnp.type.value import Value


def evaluateInteger(integer, environment):
    return Value(Type.INTEGER, integer.value)
