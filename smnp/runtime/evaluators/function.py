from smnp.error.runtime import RuntimeException
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools.error import updatePos
from smnp.runtime.tools.signature import argumentsNodeToMethodSignature
from smnp.type.model import Type


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
            defaultArguments, signature = argumentsNodeToMethodSignature(node.arguments, environment)
            arguments = [ arg.variable.value for arg in node.arguments ]
            body = node.body
            environment.addCustomFunction(name, signature, arguments, body, defaultArguments)
        except RuntimeException as e:
            raise updatePos(e, node)


class BodyEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        for child in node.children:
            evaluate(child, environment)


class ReturnEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        if len(environment.callStack) > 0:
            returnValue = expressionEvaluator()(node.value, environment).value
            raise Return(returnValue)
            # Disclaimer
            # Exception system usage to control program execution flow is really bad idea.
            # However because of lack of 'goto' instruction equivalent in Python
            # there is a need to use some mechanism to break function execution on 'return' statement
            # and immediately go to Environment's method 'invokeFunction()' or 'invokeMethod()',
            # which can handle value that came with exception and return it to code being executed.
        else:
            raise RuntimeException("Cannot use 'return' statement outside a function or method", node.pos, environment)


class Return(Exception):
    def __init__(self, value):
        if value is None:
            value = Type.void()

        self.value = value