from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class NoteEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.note(node.value)