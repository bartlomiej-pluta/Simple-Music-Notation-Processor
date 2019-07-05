from smnp.newast.node.access import AccessNode
from smnp.newast.node.args import ArgumentsListNode
from smnp.newast.node.assignment import AssignmentNode
from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.invocation import FunctionCall
from smnp.newast.parser import Parser
from smnp.token.type import TokenType


class IdentifierNode(AccessNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]

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
            ExpressionNode.parse,
            createNode=createNode
        )

    @staticmethod
    def _functionCallParser():
        def createNode(name, arguments):
            node = FunctionCall(name.pos)
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
