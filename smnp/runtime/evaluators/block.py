from smnp.runtime.evaluator import evaluate, Evaluator


class BlockEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        environment.appendScope()

        for child in node.children:
            evaluate(child, environment)

        environment.popScope()

#
# def evaluateBlock(block, environment):
#     environment.scopes.append({})
#     for node in flatListNode(block):
#         evaluate(node, environment)
#     environment.scopes.pop(-1)
#

