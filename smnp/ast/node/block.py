from smnp.ast.node.model import Node


class BlockNode(Node):
    pass


class BlockItemNode(Node):
    def __init__(self, statement, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.append(statement)

        self.statement = self.children[0]


class CloseBlockNode(Node):
    pass