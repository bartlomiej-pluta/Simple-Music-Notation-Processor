from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type
from smnp.type.value import Value


class NoteEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Value(Type.NOTE, node.value)