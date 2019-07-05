from smnp.ast.node.ret import ReturnNode
from smnp.ast.parsers.expression import parseExpression
from smnp.token.type import TokenType


def parseReturn(input, parent):
    if input.isCurrent(TokenType.RETURN):
        token = input.current()
        input.ahead()

        expr = parseExpression(input, parent)

        node = ReturnNode(expr, parent, token.pos)
        expr.parent = node

        return node
    return None