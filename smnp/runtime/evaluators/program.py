from smnp.runtime.evaluator import Evaluator, evaluate


class ProgramEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        for n in node.children:
            evaluate(n, environment)