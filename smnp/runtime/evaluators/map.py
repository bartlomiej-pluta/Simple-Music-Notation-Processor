from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type


class MapEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        map = {}
        exprEvaluator = expressionEvaluator(doAssert=True)
        for entry in node.children:
            key = exprEvaluator(entry.key, environment).value
            if key in map:
                raise RuntimeException(f"Duplicated key '{key.stringify()}' found in map", entry.pos)
            map[key] = exprEvaluator(entry.value, environment).value

        return Type.map(map)