from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.term import TermParser
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Expression(Valuable):
    pass


ExpressionParser = Parser.leftAssociativeOperatorParser(TermParser, [TokenType.PLUS, TokenType.MINUS], TermParser,
                                                        lambda left, op, right: Expression.withValue(BinaryOperator.withValues(left, op, right)))

#
# class ExpressionNode(Node):
#     def __init__(self, pos):
#         super().__init__(pos, [NoneNode()])
#
#     @property
#     def value(self):
#         return self[0]
#
#
#     @value.setter
#     def value(self, v):
#         self[0] = v
#
#
#     @classmethod
#     def withValue(cls, val, pos):
#         node = cls(pos)
#         node.value = val
#         return node
#
#     @classmethod
#     def _parse(cls, input):
#         return Parser.oneOf(
#             cls._asteriskParser(),
#             cls._expressionParser(),
#         )(input)
#
#     @classmethod
#     def _asteriskParser(cls):
#         def createNode(iterator, asterisk, statement):
#             node = AsteriskNode(asterisk.pos)
#             node.iterator = iterator
#             node.statement = statement
#             return node
#
#         return Parser.allOf(
#             cls._expressionParser(),
#             Parser.terminalParser(TokenType.ASTERISK),
#             Parser.doAssert(StatementNode.parse, 'statement'),
#             createNode=createNode
#         )
#
#     @classmethod
#     def _expressionParser(cls):
#         from smnp.ast.node.integer import IntegerLiteralNode
#         from smnp.ast.node.string import StringLiteralNode
#         from smnp.ast.node.note import NoteLiteralNode
#         from smnp.ast.node.bool import BoolLiteralNode
#         from smnp.ast.node.identifier import IdentifierNode
#         from smnp.ast.node.list import List
#         from smnp.ast.node.map import MapNode
#         from smnp.ast.node.type import TypeNode
#
#         return Parser.oneOf(
#             IntegerLiteralNode.parse,
#             StringLiteralNode.parse,
#             NoteLiteralNode.parse,
#             BoolLiteralNode.parse,
#             IdentifierNode.parse,
#             MapNode.parse,
#             List.parse,
#             TypeNode.parse,
#         )