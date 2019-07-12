from smnp.ast.node.expression import ExpressionParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.statement import StatementParser
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class IfElse(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode(), NoneNode()]

    @property
    def condition(self):
        return self[0]

    @condition.setter
    def condition(self, value):
        self[0] = value

    @property
    def ifNode(self):
        return self[1]

    @ifNode.setter
    def ifNode(self, value):
        self[1] = value

    @property
    def elseNode(self):
        return self[2]

    @elseNode.setter
    def elseNode(self, value):
        self[2] = value

    @classmethod
    def createNode(cls, ifNode, condition, elseNode=NoneNode()):
        node = cls(ifNode.pos)
        node.ifNode = ifNode
        node.condition = condition
        node.elseNode = elseNode
        return node


def IfElseStatementParser(input):
    ifStatementParser = Parser.allOf(
        Parser.terminal(TokenType.IF),
        Parser.doAssert(Parser.terminal(TokenType.OPEN_PAREN), TokenType.OPEN_PAREN.key),
        Parser.doAssert(ExpressionParser, "expression"),
        Parser.doAssert(Parser.terminal(TokenType.CLOSE_PAREN), TokenType.CLOSE_PAREN.key),
        Parser.doAssert(StatementParser, "statement"),
        createNode=lambda _, __, condition, ___, ifStatement: IfElse.createNode(ifStatement, condition),
        name="if statement"
    )

    ifElseStatementParser = Parser.allOf(
        Parser.terminal(TokenType.IF),
        Parser.doAssert(Parser.terminal(TokenType.OPEN_PAREN), TokenType.OPEN_PAREN.key),
        Parser.doAssert(ExpressionParser, "expression"),
        Parser.doAssert(Parser.terminal(TokenType.CLOSE_PAREN), TokenType.CLOSE_PAREN.key),
        Parser.doAssert(StatementParser, "statement"),
        Parser.terminal(TokenType.ELSE),
        StatementParser,
        createNode=lambda _, __, condition, ___, ifStatement, ____, elseStatement: IfElse.createNode(ifStatement, condition, elseStatement),
        name="if-else statement"
    )

    return Parser.oneOf(
        ifElseStatementParser,
        ifStatementParser,
        name="if-else/if statement"
    )(input)