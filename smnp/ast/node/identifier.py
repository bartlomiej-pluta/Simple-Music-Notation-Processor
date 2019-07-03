from smnp.ast.node.model import Node


class IdentifierNode(Node):
    def __init__(self, identifier, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.append(identifier)

        self.identifier = self.children[0]