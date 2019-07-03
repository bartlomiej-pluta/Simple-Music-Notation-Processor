from smnp.ast.node.asterisk import AsteriskNode
from smnp.ast.parsers.statement import parseStatement
from smnp.token.type import TokenType


# asterisk -> expr '*' stmt
def parseAsterisk(expr, input, parent):
    if input.hasMore() and input.current().type == TokenType.ASTERISK:
        token = input.current()
        input.ahead()

        stmt = parseStatement(input, parent)

        asterisk = AsteriskNode(expr, stmt, parent, token.pos)
        expr.parent = asterisk
        stmt.parent = asterisk
        return asterisk
    return None