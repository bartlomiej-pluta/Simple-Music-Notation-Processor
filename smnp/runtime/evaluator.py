from smnp.ast.node.block import Block
from smnp.ast.node.condition import IfElse
from smnp.ast.node.extend import Extend
from smnp.ast.node.function import FunctionDefinition
from smnp.ast.node.imports import Import
from smnp.ast.node.program import Program
from smnp.ast.node.ret import Return
from smnp.error.runtime import RuntimeException
from smnp.type.model import Type


class Evaluator:


    @classmethod
    def evaluator(cls, node, environment):
        pass

    @classmethod
    def evaluate(cls, node, environment):
        result = cls.evaluator(node, environment)
        if result is None:
            return EvaluationResult.OK(Type.void())
        return EvaluationResult.OK(result)

    @staticmethod
    def forNodes(evaluator, *nodes):
        def nodeEvaluator(node, environment):
            if type(node) in nodes:
                return evaluator(node, environment)

            return EvaluationResult.FAIL()

        return nodeEvaluator

    @staticmethod
    def oneOf(*evaluators):
        def combinedEvaluator(node, environment):
            for evaluator in evaluators:
                result = evaluator(node, environment)
                if result.result:
                    return result

            return EvaluationResult.FAIL()

        return combinedEvaluator


class EvaluationResult():
    def __init__(self, result, value):
        if result and value is None:
            raise RuntimeError("Value musn't be None if result is set to True for EvaluationResult")
        if type(value) == EvaluationResult:
            raise RuntimeError(f"Nested EvaluationResult detected. Trying to create EvaluationResult with value = {value}")
        self.result = result
        self.value = value

    @staticmethod
    def FAIL():
        return EvaluationResult(False, None)

    @staticmethod
    def OK(value):
        return EvaluationResult(True, value)

    def __str__(self):
        return f"{'OK' if self.result else 'FAILED'}[{self.value}]"


def evaluate(node, environment):
    from smnp.runtime.evaluators.program import ProgramEvaluator

    from smnp.runtime.evaluators.expression import expressionEvaluator
    from smnp.runtime.evaluators.condition import IfElseStatementEvaluator
    from smnp.runtime.evaluators.block import BlockEvaluator
    from smnp.runtime.evaluators.imports import ImportEvaluator
    from smnp.runtime.evaluators.function import FunctionDefinitionEvaluator
    from smnp.runtime.evaluators.function import ReturnEvaluator
    from smnp.runtime.evaluators.extend import ExtendEvaluator
    result = Evaluator.oneOf(
        Evaluator.forNodes(ProgramEvaluator.evaluate, Program),
        Evaluator.forNodes(IfElseStatementEvaluator.evaluate, IfElse),
        Evaluator.forNodes(BlockEvaluator.evaluate, Block),
        Evaluator.forNodes(ImportEvaluator.evaluate, Import),
        Evaluator.forNodes(FunctionDefinitionEvaluator.evaluate, FunctionDefinition),
        Evaluator.forNodes(ReturnEvaluator.evaluate, Return),
        Evaluator.forNodes(ExtendEvaluator.evaluate, Extend),
        #Evaluator.forNodes(ImportEvaluator.evaluate, ImportNode),
        #Evaluator.forNodes(FunctionDefinitionEvaluator.evaluate, FunctionDefinitionNode),
        #Evaluator.forNodes(ExtendEvaluator.evaluate, ExtendNode),
        #Evaluator.forNodes(BlockEvaluator.evaluate, BlockNode),
        #Evaluator.forNodes(ReturnEvaluator.evaluate, ReturnNode),
        expressionEvaluator()
    )(node, environment)

    if not result.result:
        raise RuntimeException("Cannot evaluate program", node.pos)

    return result

