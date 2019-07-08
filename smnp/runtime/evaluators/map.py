from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.type.model import Type


class MapEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        keys = [ evaluate(entry.key, environment).value for entry in node.children ]
        values = [ evaluate(entry.value, environment).value for entry in node.children ]
        return Type.map(dict(zip(keys, values)))