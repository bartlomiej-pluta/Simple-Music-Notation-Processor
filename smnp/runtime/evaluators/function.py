from smnp.ast.node.none import NoneNode
from smnp.ast.node.ret import ReturnNode
from smnp.ast.node.variable import TypedVariableNode
from smnp.error.runtime import RuntimeException
from smnp.library.signature import signature, listOfMatchers, ofType, mapOfMatchers
from smnp.runtime.evaluator import Evaluator, evaluate
from smnp.runtime.evaluators.expression import expressionEvaluator
from smnp.runtime.evaluators.iterable import abstractIterableEvaluator
from smnp.runtime.tools import updatePos
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

        for child in node.children:
            if type(child) == TypedVariableNode:
                if type(child.type.specifiers) == NoneNode:
                    sign.append(ofType(child.type.type))
                elif child.type.type == Type.LIST and len(child.type.specifiers) == 1:
                    sign.append(listSpecifier(child.type.specifiers[0]))
                elif child.type.type == Type.MAP and len(child.type.specifiers) == 2:
                    sign.append(mapSpecifier(child.type.specifiers[0], child.type.specifiers[1]))
                else:
                    raise RuntimeException("Unknown type", child.pos) # Todo: Improve pointing position

        return signature(*sign)
    except RuntimeException as e:
        raise updatePos(e, node)


def listSpecifier(specifier):
    subSignature = []

    for child in specifier.children:
        if type(child.specifiers) == NoneNode:
            subSignature.append(ofType(child.type))
        elif child.type == Type.LIST and len(child.type.specifiers) == 1:
            subSignature.append(listSpecifier(child.specifiers[0]))
        elif child.type == Type.MAP and len(child.specifiers) == 2:
            subSignature.append(mapSpecifier(child.specifiers[0], child.specifiers[1]))
        else:
            raise RuntimeException("Unknown type", None)

    return listOfMatchers(*subSignature)

def mapSpecifier(keySpecifier, valueSpecifier):
    keySubSignature = []
    valueSubSignature = []

    for child in keySpecifier.children:
        if type(child.specifiers) == NoneNode:
            keySubSignature.append(ofType(child.type))
        elif child.type == Type.LIST and len(child.specifiers) == 1:
            keySubSignature.append(listSpecifier(child.specifiers[0]))
        elif child.type == Type.MAP and len(child.specifiers) == 2:
            keySubSignature.append(mapSpecifier(child.specifiers[0], child.specifiers[1]))
        else:
            raise RuntimeException("Unknown type", None)

    for child in valueSpecifier.children:
        if type(child.specifiers) == NoneNode:
            valueSubSignature.append(ofType(child.type))
        elif child.type == Type.LIST and len(child.specifiers) == 1:
            valueSubSignature.append(listSpecifier(child.specifiers[0]))
        elif child.type == Type.MAP and len(child.specifiers) == 2:
            valueSubSignature.append(mapSpecifier(child.specifiers[0], child.specifiers[1]))
        else:
            raise RuntimeException("Unknown type", None)

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