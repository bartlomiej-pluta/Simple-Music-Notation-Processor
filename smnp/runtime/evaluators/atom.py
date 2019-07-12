from smnp.runtime.evaluator import Evaluator
from smnp.type.model import Type


class IntegerEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.integer(node.value)


class StringEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.string(node.value)


class NoteEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.note(node.value)


class BoolEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.bool(node.value)


class TypeEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Type.type(node.value)