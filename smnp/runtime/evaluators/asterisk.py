from smnp.ast.node.identifier import IdentifierNode
from smnp.runtime.evaluator import evaluate
from smnp.type.model import Type
from smnp.type.value import Value


def evaluateAsterisk(asterisk, environment):
    iterator = evaluate(asterisk.iterator, environment)
    if iterator.type == Type.INTEGER:
        evaluateAsteriskForNumber(asterisk, environment, iterator)

    if iterator.type == Type.LIST:
        evaluateAsteriskForList(asterisk, environment, iterator)



def evaluateAsteriskForNumber(asterisk, environment, count):
    for i in range(count.value):
        if type(asterisk.iterator) == IdentifierNode:
            environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = Value(Type.INTEGER, i+1)
        else:
            environment.scopes[-1]["_"] = Value(Type.INTEGER, i+1)

        evaluate(asterisk.statement, environment)

    if type(asterisk.iterator) == IdentifierNode:
        del environment.scopes[-1][f"_{asterisk.iterator.identifier}"]
    else:
        del environment.scopes[-1]["_"]


def evaluateAsteriskForList(asterisk, environment, list):
    for i, v in enumerate(list.value):
        if type(asterisk.iterator) == IdentifierNode:
            environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = Value(Type.INTEGER, i+1)
            environment.scopes[-1][f"{asterisk.iterator.identifier}_"] = v
        else:
            environment.scopes[-1]["_"] = Value(Type.INTEGER, i+1)
            environment.scopes[-1]["__"] = v

        evaluate(asterisk.statement, environment)

        if type(asterisk.iterator) == IdentifierNode:
            del environment.scopes[-1][f"_{asterisk.iterator.identifier}"]
            del environment.scopes[-1][f"{asterisk.iterator.identifier}_"]
        else:
            del environment.scopes[-1]["_"]
            del environment.scopes[-1]["__"]