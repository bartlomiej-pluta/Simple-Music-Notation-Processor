from smnp.ast.node.none import NoneNode
from smnp.function.signature import signature
from smnp.runtime.evaluator import Evaluator
from smnp.runtime.tools.signature import argumentsNodeToMethodSignature, listSpecifier, mapSpecifier
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType


class ExtendEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        type = cls._typeToMethodSignature(node.type)  # TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
        variable = node.variable.value
        cls._evaluateExtend(node.methods, environment, type, variable)

    @classmethod
    def _typeToMethodSignature(cls, node):
        if type(node.specifiers) == NoneNode:
            return signature(ofType(node.type.value))

        elif node.type.value == Type.LIST:
            return signature(listSpecifier(node.specifiers[0]))
        elif node.type.value == Type.MAP:
            return signature(mapSpecifier(node.specifiers[0], node.specifiers[1]))

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

