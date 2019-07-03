from smnp.ast.node.model import Node


class AssignmentNode(Node):
    def __init__(self, target, value, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([target, value])

        self.target = self.children[0]
        self.value = self.children[1]