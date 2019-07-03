from smnp.ast.node.model import Node


class FunctionCallNode(Node):
    def __init__(self, identifier, arguments, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([identifier, arguments])

        self.identifier = self.children[0]
        self.arguments = self.children[1]


class FunctionDefinitionNode(Node):
    def __init__(self, name, parameters, body, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([name, parameters, body])

        self.name = self.children[0]
        self.parameters = self.children[1]
        self.body = self.children[2]