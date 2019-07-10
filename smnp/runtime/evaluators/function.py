from smnp.ast.node.none import NoneNode
from smnp.ast.node.ret import ReturnNode
from smnp.ast.node.type import TypeNode
from smnp.error.runtime import RuntimeException
from smnp.function.signature import signature, varargSignature
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools import updatePos
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOfMatchers
from smnp.type.signature.matcher.map import mapOfMatchers
from smnp.type.signature.matcher.type import ofType, oneOf, allTypes


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
            e.pos = node.pos
            raise e


def argumentsNodeToMethodSignature(node):
    try:
        sign = []
        vararg = None
        argumentsCount = len(node.children)
        for i, child in enumerate(node.children):
            if type(child.type) == TypeNode:
                if child.vararg:
                    if i != argumentsCount-1:
                        raise RuntimeException("Vararg must be the last argument in signature", child.pos)
                    vararg = typeMatcher(child.type)
                else:
                    sign.append(typeMatcher(child.type))
            elif type(child.type) == NoneNode:
                if child.vararg:
                    if i != argumentsCount-1:
                        raise RuntimeException("Vararg must be the last argument in signature", child.pos)
                    vararg = allTypes()
                else:
                    sign.append(allTypes())
            else:
                if child.vararg:
                    if i != argumentsCount-1:
                        raise RuntimeException("Vararg must be the last argument in signature", child.pos)
                    vararg = multipleTypeMatcher(child)
                else:
                    sign.append(multipleTypeMatcher(child))


        return varargSignature(vararg, *sign, wrapVarargInValue=True) if vararg is not None else signature(*sign)
    except RuntimeException as e:
        raise updatePos(e, node)


def multipleTypeMatcher(typeNode):
    subSignature = []

    for child in typeNode.type.children:
        m = typeMatcher(child)
        subSignature.append(m)

    return oneOf(*subSignature)


def typeMatcher(typeNode):
    if type(typeNode.specifiers) == NoneNode:
        return ofType(typeNode.type)
    elif typeNode.type == Type.LIST and len(typeNode.specifiers) == 1:
        return listSpecifier(typeNode.specifiers[0])
    elif typeNode.type == Type.MAP and len(typeNode.specifiers) == 2:
        return mapSpecifier(typeNode.specifiers[0], typeNode.specifiers[1])

    raise RuntimeException("Unknown type", typeNode.pos)  # Todo: Improve pointing position



def listSpecifier(specifier):
    subSignature = []

    for child in specifier.children:
        subSignature.append(typeMatcher(child))

    return listOfMatchers(*subSignature)

def mapSpecifier(keySpecifier, valueSpecifier):
    keySubSignature = []
    valueSubSignature = []

    for child in keySpecifier.children:
        keySubSignature.append(typeMatcher(child))

    for child in valueSpecifier.children:
        valueSubSignature.append(typeMatcher(child))

    return mapOfMatchers(keySubSignature, valueSubSignature)


class BodyEvaluator(Evaluator):

    @classmethod
    def evaluator(cls, node, environment):
        for child in node.children:
            if type(child) == ReturnNode:
                x = expressionEvaluator(doAssert=True)(child.value, environment).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                return x
            else:
                evaluate(child, environment)

# if node.type.specifier is not NoneNode:
            #     if Type[node.type.upper()] == Type.LIST:
            #         return listOf([])

#
# def evaluateFunctionDefinition(definition, environment):
#     name = definition.name
#     params = list([p for p in flatListNode(definition.parameters)])
#     body = definition.body
#
#     if not isinstance(definition.parent, Program):
#         raise RuntimeException(f"Functions can be defined only on the top level of script", name.pos)
#
#     for p in params:
#         if not isinstance(p, IdentifierNode):
#             raise RuntimeException("Parameter of function definition must be an identifier", p.pos, )
#
#     if name.identifier in environment.customFunctions or name.identifier in environment.functions:
#         raise RuntimeException(f"Function '{name.identifier}' already exists", name.pos)
#
#     environment.customFunctions[name.identifier] = {
#         'params': params,
#         'body': flatListNode(body)
#     }
#
#
# def evaluateFunctionCall(functionCall, environment):
#     try:
#         functionName = functionCall.identifier.identifier
#         arguments = evaluateList(functionCall.arguments, environment).value
#         return environment.invokeFunction(functionName, arguments)
#     except SmnpException as e:
#         e.pos = functionCall.pos
#         raise e


# def evaluateFunctionCall(functionCall, environment):
#     funcName = functionCall.identifier.identifier
#     arguments = evaluateList(functionCall.arguments, environment)
#     for name, function in environment.customFunctions.items():
#         if funcName == name:
#             if len(function['params']) != len(arguments):
#                 raise RuntimeException(functionCall.pos, f"Calling '{funcName}' requires {len(function['params'])} and {len(arguments)} was passed")
#             environment.scopes.append({ function['params'][i].identifier: v for i, v in enumerate(arguments) })
#             returnValue = None
#             for node in function['body']:
#                 if not isinstance(node, ReturnNode):
#                     evaluate(node, environment)
#                 else:
#                     returnValue = evaluateReturn(node, environment)
#             environment.scopes.pop(-1)
#             return returnValue
#     for name, definition in environment.functions.items():
#         if name == funcName:
#             return definition(arguments, environment)
#     raise RuntimeException(functionCall.pos, f"Function '{funcName}' does not exist")