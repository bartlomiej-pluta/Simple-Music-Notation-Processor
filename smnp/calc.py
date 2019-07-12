from smnp.ast.node.model import Node
from smnp.ast.parser import Parser
from smnp.token.tokenizer import tokenize
from smnp.token.type import TokenType


class Atom(Node):
    def __init__(self, value, pos):
        super().__init__(pos)
        self.children = [value]

    @property
    def value(self):
        return self[0]

class Operation(Node):
    def __init__(self, left, op, right, pos):
        super().__init__(pos)
        self.children = [left, op, right]

    @property
    def left(self):
        return self[0]

    @property
    def operator(self):
        return self[1]

    @property
    def right(self):
        return self[2]

def atom():
    return Parser.oneOfTerminals(TokenType.INTEGER, TokenType.NOTE, TokenType.STRING, createNode=lambda val, pos: Atom(val, pos))

def chain():
    return Parser.leftAssociativeOperatorParser(atom(), [TokenType.DOT], atom(), lambda left, op, right: Operation(left, op, right, op.pos), name="chain")

def factor():
    return Parser.leftAssociativeOperatorParser(chain(), [TokenType.DOUBLE_ASTERISK], chain(), lambda left, op, right: Operation(left, op, right, op.pos), name="factor")

def term():
    return Parser.leftAssociativeOperatorParser(factor(), [TokenType.ASTERISK, TokenType.SLASH], factor(), lambda left, op, right: Operation(left, op, right, op.pos), name="term")

def expr():
    return Parser.leftAssociativeOperatorParser(term(), [TokenType.PLUS, TokenType.MINUS], term(), lambda left, op, right: Operation(left, op, right, op.pos), name="expr")
#
def evaluate(node):
    if type(node) == Atom:
        return node.value
    lhs = evaluate(node.left)
    rhs = evaluate(node.right)
    return {
        "+": int(lhs) + int(rhs),
        "*": int(lhs) * int(rhs),
        "-": int(lhs) - int(rhs),
        "/": int(lhs) / int(rhs),
        "**": int(lhs) ** int(rhs)
    }[node.operator.value]

def draft():

    tokens = tokenize(['"fesf fe" + "fsefsef" + "fsefs"'])
    e = expr()
    node = e(tokens).node
    node.print()
