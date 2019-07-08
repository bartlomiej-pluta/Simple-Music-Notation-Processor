from smnp.runtime.evaluator import Evaluator
from smnp.runtime.evaluators.function import argumentsNodeToMethodSignature
from smnp.runtime.evaluators.type import TypeEvaluator


class ExtendEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        type = TypeEvaluator.evaluate(node.type, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
        variable = node.variable.value
        cls._evaluateExtend(node.methods, environment, type, variable)

    @classmethod
    def _evaluateExtend(cls, node, environment, type, variable):
        for child in node.children:
            cls._evaluateMethodDefinition(child, environment, type, variable)

    @classmethod
    def _evaluateMethodDefinition(cls, node, environment, type, variable):
        name = node.name.value
        signature = argumentsNodeToMethodSignature(node.arguments)
        arguments = [arg.variable.value for arg in node.arguments]
        body = node.body
        environment.addCustomMethod(type, variable, name, signature, arguments, body)