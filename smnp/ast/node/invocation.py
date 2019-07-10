from smnp.ast.node.access import LeftAssociativeOperatorNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class ArgumentsListNode(Node):

    @classmethod
    def _parse(cls, input):
        return abstractIterableParser(ArgumentsListNode, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN,
                                      Parser.doAssert(ExpressionNode.parse, "expression"))(input)


class FunctionCallNode(LeftAssociativeOperatorNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode()]

    @property
    def name(self):
        return self[0]

    @name.setter
    def name(self, value):
        self[0] = value

    @property
    def arguments(self):
        return self[1]

    @arguments.setter
    def arguments(self, value):
        self[1] = value

    @classmethod
    def _parse(cls, input):
        raise RuntimeError("This class is not supposed to be automatically called")

