from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import evaluate
from smnp.runtime.tools import flatListNode
from smnp.type.model import Type
from smnp.type.value import Value


def evaluateList(list, environment):
    newList = []
    for elem in flatListNode(list):
        item = evaluate(elem, environment)
        if item.type == Type.VOID:
            raise RuntimeException(f"Expected expression, found '{item.type.name}'", elem.pos)
        newList.append(item)
    return Value(Type.LIST, newList)


