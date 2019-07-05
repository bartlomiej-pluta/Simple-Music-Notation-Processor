from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.model import Node, ParseResult
from smnp.newast.node.none import NoneNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


def abstractIterableParser(iterableNodeType, openTokenType, closeTokenType, itemParser):
    class AbstractIterableTailNode(ExpressionNode):
        def __init__(self, pos):
            super().__init__(pos)

            self.children.append(NoneNode())

        @property
        def next(self):
            return self[1]

        @next.setter
        def next(self, value):
            self[1] = value

        @classmethod
        def _parse(cls, input):
            return Parser.oneOf(
                AbstractIterableTailNode._parser1(),
                AbstractIterableTailNode._parser2(),
            )(input)
        
        @staticmethod
        def _parser1():
            return Parser.terminalParser(closeTokenType)
        
        @staticmethod
        def _parser2():
            def createNode(comma, expr, iterableTail):
                node = AbstractIterableTailNode(expr.pos)
                node.value = expr
                node.next = iterableTail
                return node

            return Parser.allOf(
                Parser.terminalParser(TokenType.COMMA),
                itemParser,
                AbstractIterableTailNode.parse,
                createNode=createNode
            )


    class AbstractIterableNode(ExpressionNode):
        def __init__(self, pos):
            super().__init__(pos)

            self.children.append(NoneNode())

        @property
        def next(self):
            return self[1]

        @next.setter
        def next(self, value):
            self[1] = value

        @classmethod
        def _parse(cls, input):
            return Parser.oneOf(
                AbstractIterableNode._parser1(),
                AbstractIterableNode._parser2()
            )(input)
        
        @staticmethod
        def _parser1():
            def emptyIterable(openToken, closeToken):
                node = AbstractIterableNode(openToken.pos)
                node.value = openToken
                node.next = closeToken
                return node

            return Parser.allOf(
                Parser.terminalParser(openTokenType),
                Parser.terminalParser(closeTokenType),
                createNode=emptyIterable
            )


        @staticmethod
        def _parser2():
            def createNode(openParen, expr, iterableTail):
                node = AbstractIterableNode(openParen.pos)
                node.value = expr
                node.next = iterableTail
                return node

            return Parser.allOf(
                Parser.terminalParser(openTokenType, lambda v, pos: Node(pos)),
                itemParser,
                AbstractIterableTailNode.parse,
                createNode=createNode
            )

    def toDesiredType(parser):
        def parse(input):
            result = parser(input)
            if result.result:
                node = iterableNodeType(result.node.pos)
                node.children.clear()
                node.children.extend([ result.node.value, result.node.next ])
                return ParseResult.OK(node)

            return ParseResult.FAIL()

        return parse

    return toDesiredType(AbstractIterableNode.parse)