from smnp.runtime.evaluator import evaluate


def evaluateReturn(returnNode, environment):
    return evaluate(returnNode.value, environment)