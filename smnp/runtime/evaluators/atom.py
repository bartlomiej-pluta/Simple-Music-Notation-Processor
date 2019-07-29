from smnp.ast.node.atom import StringLiteral, IntegerLiteral, NoteLiteral, BoolLiteral, TypeLiteral, FloatLiteral
from smnp.ast.node.identifier import Identifier
from smnp.ast.node.list import List
from smnp.ast.node.map import Map
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator, EvaluationResult
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.float import FloatEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools.error import updatePos
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
        keyEvaluator = Evaluator.oneOf(
            Evaluator.forNodes(lambda node, environment: EvaluationResult.OK(Type.string(node.value)), Identifier),
            expressionEvaluator(doAssert=True)
        )
        for entry in node.children:
            key = keyEvaluator(entry.key, environment).value
            if key in map:
                raise RuntimeException(f"Duplicated key '{key.stringify()}' found in map", entry.pos)
            map[key] = expressionEvaluator(doAssert=True)(entry.value, environment).value

        return Type.map(map)


class IdentifierEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        try:
            return environment.findVariable(node.value)
        except RuntimeException as e:
            raise updatePos(e, node)


class AtomEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        return Evaluator.oneOf(
            Evaluator.forNodes(StringEvaluator.evaluate, StringLiteral),
            Evaluator.forNodes(IntegerEvaluator.evaluate, IntegerLiteral),
            Evaluator.forNodes(FloatEvaluator.evaluate, FloatLiteral),
            Evaluator.forNodes(NoteEvaluator.evaluate, NoteLiteral),
            Evaluator.forNodes(BoolEvaluator.evaluate, BoolLiteral),
            Evaluator.forNodes(TypeEvaluator.evaluate, TypeLiteral),
            Evaluator.forNodes(IdentifierEvaluator.evaluate, Identifier),
            Evaluator.forNodes(ListEvaluator.evaluate, List),
            Evaluator.forNodes(MapEvaluator.evaluate, Map)
        )(node, environment).value
