from smnp.ast.node.assignment import AssignmentNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.invocation import FunctionCallNode, ArgumentsListNode
from smnp.ast.node.operator import LeftAssociativeOperatorNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class IdentifierNode(LeftAssociativeOperatorNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @classmethod
    def _literalParser(cls):
        return Parser.oneOf(
            IdentifierNode._functionCallParser(),
            IdentifierNode._assignmentParser(),
            IdentifierNode.identifierParser()
        )

    @staticmethod
    def _assignmentParser():
        def createNode(target, assignment, value):
            node = AssignmentNode(assignment.pos)
            node.target = target
            node.value = value
            return node

        return Parser.allOf(
            IdentifierNode.identifierParser(),
            Parser.terminalParser(TokenType.ASSIGN),
            Parser.doAssert(ExpressionNode.parse, "expression"),
            createNode=createNode
        )

    @staticmethod
    def _functionCallParser():
        def createNode(name, arguments):
            node = FunctionCallNode(name.pos)
            node.name = name
            node.arguments = arguments
            return node

        return Parser.allOf(
            IdentifierNode.identifierParser(),
            ArgumentsListNode.parse,
            createNode=createNode
        )

    @staticmethod
    def identifierParser():
        return Parser.terminalParser(TokenType.IDENTIFIER, lambda val, pos: IdentifierNode.withValue(val, pos))
