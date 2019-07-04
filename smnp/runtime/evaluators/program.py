from smnp.runtime.evaluator import evaluate


def evaluateProgram(program, environment):
    for node in program.children:
        evaluate(node, environment)