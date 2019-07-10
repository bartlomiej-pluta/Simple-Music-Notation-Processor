from smnp.ast.node.none import NoneNode
from smnp.ast.node.type import TypeNode, TypeSpecifier
from smnp.error.runtime import RuntimeException
from smnp.function.signature import varargSignature, signature
from smnp.runtime.tools.error import updatePos
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOfMatchers
from smnp.type.signature.matcher.map import mapOfMatchers
from smnp.type.signature.matcher.type import allTypes, oneOf, ofType


def argumentsNodeToMethodSignature(node):
    try:
        sign = []
        vararg = None
        argumentsCount = len(node.children)
        for i, child in enumerate(node.children):
            matchers = {
                TypeNode: (lambda c: c.type, typeMatcher),
                NoneNode: (lambda c: c.type, lambda c: allTypes()),
                TypeSpecifier: (lambda c: c, multipleTypeMatcher)
            }
            evaluatedMatcher = matchers[type(child.type)][1](matchers[type(child.type)][0](child))
            if child.vararg:
                if i != argumentsCount - 1:
                    raise RuntimeException("Vararg must be the last argument in signature", child.pos)
                vararg = evaluatedMatcher
            else:
                sign.append(evaluatedMatcher)


        return varargSignature(vararg, *sign, wrapVarargInValue=True) if vararg is not None else signature(*sign)
    except RuntimeException as e:
        raise updatePos(e, node)


def multipleTypeMatcher(typeNode):
    subSignature = []

    if len(typeNode.type.children) == 0:
        return allTypes()

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

    if len(specifier.children) == 0:
        subSignature.append(allTypes())

    for child in specifier.children:
        subSignature.append(typeMatcher(child))

    return listOfMatchers(*subSignature)


def mapSpecifier(keySpecifier, valueSpecifier):
    keySubSignature = []
    valueSubSignature = []

    if len(keySpecifier.children) == 0:
        keySubSignature.append(allTypes())

    if len(valueSpecifier.children) == 0:
        valueSubSignature.append(allTypes())

    for child in keySpecifier.children:
        keySubSignature.append(typeMatcher(child))

    for child in valueSpecifier.children:
        valueSubSignature.append(typeMatcher(child))

    return mapOfMatchers(keySubSignature, valueSubSignature)