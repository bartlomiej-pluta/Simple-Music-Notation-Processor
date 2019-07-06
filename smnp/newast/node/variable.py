from smnp.newast.node.expression import ExpressionNode
from smnp.newast.node.identifier import IdentifierNode
from smnp.newast.node.none import NoneNode
from smnp.newast.node.type import TypeNode
from smnp.newast.parser import Parser
from smnp.token.type import TokenType

class TypedVariableNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children.append(NoneNode())

    @property
    def type(self):
        return self[0]

    @type.setter
    def type(self, value):
        self[0] = value

    @property
    def variable(self):
        return self[1]

    @variable.setter
    def variable(self, value):
        self[1] = value

    @classmethod
    def parser(cls):
        def createNode(type, variable):
            node = TypedVariableNode(type.pos)
            node.type = type
            node.variable = variable
            return node

        return Parser.allOf(
            Parser.terminalParser(TokenType.TYPE, lambda val, pos: TypeNode.withValue(val, pos)),
            IdentifierNode.identifierParser(),
            createNode=createNode
        )

    @classmethod
    def _parse(cls, input):
        #TODO
        raise RuntimeError("Not implemented yet. There is still required work to correctly build AST related to IdentifierNode")