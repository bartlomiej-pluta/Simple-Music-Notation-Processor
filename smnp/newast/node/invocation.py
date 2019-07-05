from smnp.newast.node.access import AccessNode


class FunctionCall(AccessNode):
    def __init__(self, pos):
        super().__init__(pos)

    @property
    def name(self):
        return self[0]

    @name.setter
    def name(self, value):
        self[0] = value

    @property
    def arguments(self):
        return self[1]

    @arguments.setter
    def arguments(self, value):
        self[1] = value

    @classmethod
    def _parse(cls, input):
        raise RuntimeError("This class is not supposed to be automatically called")

