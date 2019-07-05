from smnp.newast.node.model import Node


class IgnoredNode(Node):
    def __init__(self, pos):
        super().__init__(pos)
