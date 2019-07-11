from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.node.model import Node, ParseResult
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


def abstractIterableParser(iterableNodeType, openTokenType, closeTokenType, itemParser):

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

    def abstractIterableParser(input):
        return Parser.oneOf(
            emptyIterable,
            openIterable
        )(input)

    def emptyIterable(input):
        def createNode(open, close):
            node = AbstractIterable(open.pos)
            node.value = open
            node.next = close
            return node

        return Parser.allOf(
            Parser.terminalParser(openTokenType),
            Parser.terminalParser(closeTokenType),
            createNode=createNode
        )(input)

    def openIterable(input):
        def createNode(open, item, tail):
            node = AbstractIterable(open.pos)
            node.value = item
            node.next = tail
            return node

        return Parser.allOf(
            Parser.terminalParser(openTokenType),
            itemParser,
            abstractIterableTailParser,
            createNode=createNode
        )(input)

    def abstractIterableTailParser(input):
        return Parser.oneOf(
            closeIterable,
            nextItem,
        )(input)

    def nextItem(input):
        def createNode(comma, item, tail):
            node = AbstractIterableTail(item.pos)
            node.value = item
            node.next = tail
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.COMMA, doAssert=True),
            itemParser,
            abstractIterableTailParser,
            createNode=createNode
        )(input)

    def closeIterable(input):
        return Parser.terminalParser(closeTokenType)(input)


    return toFlatDesiredNode(iterableNodeType, abstractIterableParser)


def toFlatDesiredNode(iterableNodeType, parser):
    def parse(input):
        result = parser(input)

        if result.result:
            value = flattenList(result.node)
            node = iterableNodeType(result.node.pos)
            node.children.clear()
            for v in value:
                node.append(v)
            return ParseResult.OK(node)

        return ParseResult.FAIL()

    return Parser(parse, "flat", [parser])


def flattenList(node, output=None):
    if output is None:
        output = []

    if type(node.value) != IgnoredNode:
        output.append(node.value)

    if type(node.next) != IgnoredNode:
        flattenList(node.next, output)

    return output
