from smnp.ast.node.model import Node


class AsteriskNode(Node):
    def __init__(self, iterator, statement, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([iterator, statement])

        self.iterator = self.children[0]
        self.statement = self.children[1]