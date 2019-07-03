from smnp.ast.node.model import Node


class ListNode(Node):
    pass


class ListItemNode(Node):
    def __init__(self, value, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.append(value)

        self.value = self.children[0]


class CloseListNode(Node):
    pass