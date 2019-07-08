from smnp.ast.node.identifier import IdentifierNode
from smnp.runtime.evaluator import evaluate, Evaluator, EvaluationResult
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.type.model import Type
from smnp.type.value import Value


class AsteriskEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        iterator = expressionEvaluator(doAssert=True)(node.iterator, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
        return Evaluator.oneOf(
            cls._numberIteratorAsteriskEvaluator(iterator),
            cls._listIteratorAsteriskEvaluator(iterator)
        )(node, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult

    @classmethod
    def _numberIteratorAsteriskEvaluator(cls, evaluatedIterator):
        def evaluator(node, environment):
            if evaluatedIterator.type == Type.INTEGER:
                results = []
                automaticVariable = cls._automaticNamedVariable(node.iterator, environment, "_")
                for i in range(evaluatedIterator.value):
                    environment.scopes[-1][automaticVariable] = Value(Type.INTEGER, i + 1)
                    result = evaluate(node.statement, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                    if result is not None and result.type != Type.VOID:
                        results.append(result)

                del environment.scopes[-1][automaticVariable]

                return EvaluationResult.OK(Value(Type.LIST, results).decompose())

            return EvaluationResult.FAIL()

        return evaluator

    @classmethod
    def _automaticNamedVariable(cls, iteratorNode, environment, prefix=''):
        if type(iteratorNode) == IdentifierNode:
            return cls._automaticVariableName(environment, prefix, iteratorNode.value, False)
        else:
            return cls._automaticVariableName(environment, prefix, '', True)

    @classmethod
    def _automaticVariableName(cls, environment, prefix='', suffix='', startWithNumber=False):
        number = 1 if startWithNumber else ''
        variableName = lambda x: f"{prefix}{x}{suffix}"
        while environment.findVariableScope(variableName(number)) is not None:
            if number == '':
                number = 1
            else:
                number += 1

        return variableName(number)

    @classmethod
    def _listIteratorAsteriskEvaluator(cls, evaluatedIterator):
        def evaluator(node, environment):
            if evaluatedIterator.type == Type.LIST:
                results = []
                automaticVariableKey = cls._automaticNamedVariable(node.iterator, environment, "_")
                automaticVariableValue = cls._automaticNamedVariable(node.iterator, environment, "__")
                for i, v in enumerate(evaluatedIterator.value):
                    environment.scopes[-1][automaticVariableKey] = Value(Type.INTEGER, i + 1)
                    environment.scopes[-1][automaticVariableValue] = v
                    result = evaluate(node.statement, environment).value  # TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                    if result is not None and result.type != Type.VOID:
                        results.append(result)

                del environment.scopes[-1][automaticVariableKey]
                del environment.scopes[-1][automaticVariableValue]

                return EvaluationResult.OK(Value(Type.LIST, results).decompose())

            return EvaluationResult.FAIL()

        return evaluator

#
# def evaluateAsterisk(asterisk, environment):
#     iterator = evaluate(asterisk.iterator, environment)
#     if iterator.type == Type.INTEGER:
#         evaluateAsteriskForNumber(asterisk, environment, iterator)
#
#     if iterator.type == Type.LIST:
#         evaluateAsteriskForList(asterisk, environment, iterator)
#
#
#
# def evaluateAsteriskForNumber(asterisk, environment, count):
#     for i in range(count.value):
#         if type(asterisk.iterator) == IdentifierNode:
#             environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = Value(Type.INTEGER, i+1)
#         else:
#             environment.scopes[-1]["_"] = Value(Type.INTEGER, i+1)
#
#         evaluate(asterisk.statement, environment)
#
#     if type(asterisk.iterator) == IdentifierNode:
#         del environment.scopes[-1][f"_{asterisk.iterator.identifier}"]
#     else:
#         del environment.scopes[-1]["_"]
#
#
# def evaluateAsteriskForList(asterisk, environment, list):
#     for i, v in enumerate(list.value):
#         if type(asterisk.iterator) == IdentifierNode:
#             environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = Value(Type.INTEGER, i+1)
#             environment.scopes[-1][f"{asterisk.iterator.identifier}_"] = v
#         else:
#             environment.scopes[-1]["_"] = Value(Type.INTEGER, i+1)
#             environment.scopes[-1]["__"] = v
#
#         evaluate(asterisk.statement, environment)
#
#         if type(asterisk.iterator) == IdentifierNode:
#             del environment.scopes[-1][f"_{asterisk.iterator.identifier}"]
#             del environment.scopes[-1][f"{asterisk.iterator.identifier}_"]
#         else:
#             del environment.scopes[-1]["_"]
#             del environment.scopes[-1]["__"]
