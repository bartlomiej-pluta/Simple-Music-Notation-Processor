from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.node.model import Node, ParseResult
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parsers, DecoratorParser
from smnp.token.type import TokenType


def abstractIterableParser(iterableNodeType, openTokenType, closeTokenType, itemParser, name):

    class AbstractIterable(Node):
        def __init__(self, pos):
            super().__init__(pos)
            self.children = [NoneNode(), NoneNode()]

        @property
        def value(self):
            return self[0]

        @value.setter
        def value(self, value):
            self[0] = value

        @property
        def next(self):
            return self[1]

        @next.setter
        def next(self, value):
            self[1] = value

    class AbstractIterableTail(AbstractIterable):
        pass

    def abstractIterableParser():
        return Parsers.oneOf(
            emptyIterable(),
            openIterable(),
            name=name
        )

    def emptyIterable():
        def createNode(open, close):
            node = AbstractIterable(open.pos)
            node.value = open
            node.next = close
            return node

        return Parsers.allOf(
            Parsers.terminal(openTokenType),
            Parsers.terminal(closeTokenType),
            createNode=createNode,
            name=name+"Empty"
        )

    def openIterable():
        def createNode(open, item, tail):
            node = AbstractIterable(open.pos)
            node.value = item
            node.next = tail
            return node

        return Parsers.allOf(
            Parsers.terminal(openTokenType),
            itemParser,
            abstractIterableTailParser(),
            createNode=createNode,
            name=name+"Open"
        )

    def abstractIterableTailParser():
        return Parsers.oneOf(
            closeIterable(),
            nextItem(),
            name=name+"Tail"
        )

    def nextItem():
        def createNode(comma, item, tail):
            node = AbstractIterableTail(item.pos)
            node.value = item
            node.next = tail
            return node

        return Parsers.allOf(
            Parsers.terminal(TokenType.COMMA, doAssert=True),
            itemParser,
            abstractIterableTailParser(),
            name=name+"NextItem",
            createNode=createNode
        )

    def closeIterable():
        return Parsers.terminal(closeTokenType)


    return abstractIterableParser()
    #return toFlatDesiredNode(iterableNodeType, abstractIterableParser())


def toFlatDesiredNode(iterableNodeType, parser):
    def wrapper(result):
        if result.result:
            value = flattenList(result.node)
            node = iterableNodeType(result.node.pos)
            node.children.clear()
            for v in value:
                node.append(v)
            return ParseResult.OK(node)

        return ParseResult.FAIL()

    return DecoratorParser(wrapper, parser)


def flattenList(node, output=None):
    if output is None:
        output = []

    if type(node.value) != IgnoredNode:
        output.append(node.value)

    if type(node.next) != IgnoredNode:
        flattenList(node.next, output)

    return output
