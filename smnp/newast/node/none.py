from smnp.newast.node.model import Node


class NoneNode(Node):
    def __init__(self):
        super().__init__((-1, -1))

    def _parse(self, input):
        pass