from smnp.newast.node.none import NoneNode
from smnp.newast.node.statement import StatementNode


class AsteriskNode(StatementNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode()]

    @property
    def iterator(self):
        return self[0]

    @iterator.setter
    def iterator(self, value):
        self[0] = value

    @property
    def statement(self):
        return self[1]

    @statement.setter
    def statement(self, value):
        self[1] = value

    @classmethod
    def _parse(cls, input):
        raise RuntimeError("This class is not supposed to be automatically called")