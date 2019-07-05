from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.model import Node
from smnp.newast.node.none import NoneNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class ListTailNode(ExpressionNode):
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
            ListTailNode._parser1(),
            ListTailNode._parser2(),
        )(input)

    # listTail := ']'
    @staticmethod
    def _parser1():
        return Parser.terminalParser(TokenType.CLOSE_PAREN)

    # listTail := ',' expr listTail
    @staticmethod
    def _parser2():
        def createNode(comma, expr, listTail):
            node = ListTailNode(expr.pos)
            node.value = expr
            node.next = listTail
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.COMMA),
            ExpressionNode.parse,
            ListTailNode.parse,
            createNode=createNode
        )


class ListNode(ExpressionNode):
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
            ListNode._parser1(),
            ListNode._parser2()
        )(input)

    # list := '[' ']'
    @staticmethod
    def _parser1():
        def emptyList(openParen, closeParen):
            node = ListNode(openParen.pos)
            node.value = openParen
            node.next = closeParen
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.OPEN_PAREN),
            Parser.terminalParser(TokenType.CLOSE_PAREN),
            createNode=emptyList
        )


    # '[' expr listTail
    @staticmethod
    def _parser2():
        def createNode(openParen, expr, listTail):
            node = ListNode(openParen.pos)
            node.value = expr
            node.next = listTail
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.OPEN_PAREN, lambda v, pos: Node(pos)),
            ExpressionNode.parse,
            ListTailNode.parse,
            createNode=createNode
        )
