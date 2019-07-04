from smnp.ast.node.colon import ColonNode
from smnp.ast.parsers.expression import parseExpression
from smnp.error.syntax import SyntaxException
from smnp.token.type import TokenType


# colon -> expr ':' expr
def parseColon(expr1, input, parent):
    if input.hasCurrent() and input.current().type == TokenType.COLON:
        token = input.current()
        input.ahead()
        expr2 = parseExpression(input, parent)

        if expr2 is None:
            raise SyntaxException(f"Expected expression '{input.current().value}'", input.current().pos)
        colon = ColonNode(expr1, expr2, parent, token.pos)
        expr1.parent = colon
        expr2.parent = colon
        return colon
    return None