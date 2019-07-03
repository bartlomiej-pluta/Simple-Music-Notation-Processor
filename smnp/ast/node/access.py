from smnp.ast.node.model import Node


class AccessNode(Node):
    def __init__(self, element, property, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([element, property])

        self.element = self.children[0]
        self.property = self.children[1]