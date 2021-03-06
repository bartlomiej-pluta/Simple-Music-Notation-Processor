from smnp.ast.node.atom import StringParser
from smnp.ast.node.model import Node
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Import(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [None]

    @property
    def source(self):
        return self[0]

    @source.setter
    def source(self, value):
        self[0] = value

    @classmethod
    def withValue(cls, value):
        node = cls(value.pos)
        node.source = value
        return node


def ImportParser(input):
    return Parser.allOf(
        Parser.terminal(TokenType.IMPORT),
        Parser.doAssert(StringParser, "import source as string"),
        createNode=lambda imp, source: Import.withValue(source),
        name="import"
    )(input)
