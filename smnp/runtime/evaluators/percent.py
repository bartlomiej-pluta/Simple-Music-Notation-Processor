from smnp.type.model import Type
from smnp.type.value import Value


def evaluatePercent(percent, environment):
    return Value(Type.PERCENT, percent.value.value * 0.01)