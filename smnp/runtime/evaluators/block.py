from smnp.runtime.evaluator import evaluate
from smnp.runtime.tools import flatListNode


def evaluateBlock(block, environment):
    environment.scopes.append({})
    for node in flatListNode(block):
        evaluate(node, environment)
    environment.scopes.pop(-1)


