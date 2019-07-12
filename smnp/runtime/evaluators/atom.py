from smnp.ast.node.atom import StringLiteral, IntegerLiteral, NoteLiteral, BoolLiteral, TypeLiteral
from smnp.ast.node.list import List
from smnp.ast.node.map import Map
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
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


class ListEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        list = abstractIterableEvaluator(expressionEvaluator(doAssert=True))(node, environment)
        return Type.list(list)


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


class AtomEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Evaluator.oneOf(
            Evaluator.forNodes(StringEvaluator.evaluate, StringLiteral),
            Evaluator.forNodes(IntegerEvaluator.evaluate, IntegerLiteral),
            Evaluator.forNodes(NoteEvaluator.evaluate, NoteLiteral),
            Evaluator.forNodes(BoolEvaluator.evaluate, BoolLiteral),
            Evaluator.forNodes(TypeEvaluator.evaluate, TypeLiteral),
            Evaluator.forNodes(ListEvaluator.evaluate, List),
            Evaluator.forNodes(MapEvaluator.evaluate, Map)
        )(node, environment).value
