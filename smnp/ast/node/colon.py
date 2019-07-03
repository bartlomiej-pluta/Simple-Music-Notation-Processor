from smnp.ast.node.model import Node


class ColonNode(Node):
    def __init__(self, a, b, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([a, b])

        self.a = self.children[0]
        self.b = self.children[1]