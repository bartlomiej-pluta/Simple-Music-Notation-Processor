from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.node.none import NoneNode
from smnp.ast.node.type import TypeNode
from smnp.ast.parser import Parser


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
            TypeNode.parse,
            Parser.doAssert(IdentifierNode.identifierParser(), "variable name"),
            createNode=createNode
        )

    @classmethod
    def _parse(cls, input):
        #TODO
        raise RuntimeError("Not implemented yet. There is still required work to correctly build AST related to IdentifierNode")
