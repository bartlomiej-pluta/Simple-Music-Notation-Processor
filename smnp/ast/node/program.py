from smnp.ast.node.model import Node


class Program(Node):
    def __init__(self):
        Node.__init__(self, None, (-1, -1))