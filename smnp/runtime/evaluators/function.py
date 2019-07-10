from smnp.ast.node.ret import ReturnNode
from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools.error import updatePos
from smnp.runtime.tools.signature import argumentsNodeToMethodSignature


class FunctionCallEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        try:
            name = node.name.value
            arguments = abstractIterableEvaluator(expressionEvaluator(True))(node.arguments, environment)
            return environment.invokeFunction(name, arguments)
        except RuntimeException as e:
            raise updatePos(e, node)


class FunctionDefinitionEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        try:
            name = node.name.value
            signature = argumentsNodeToMethodSignature(node.arguments)
            arguments = [ arg.variable.value for arg in node.arguments ]
            body = node.body
            environment.addCustomFunction(name, signature, arguments, body)
        except RuntimeException as e:
            raise updatePos(e, node)


class BodyEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        for child in node.children:
            if type(child) == ReturnNode:
                x = expressionEvaluator(doAssert=True)(child.value, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                return x
            else:
                evaluate(child, environment)

