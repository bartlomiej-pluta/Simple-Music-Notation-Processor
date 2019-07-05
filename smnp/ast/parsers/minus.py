from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.parsers.integer import parseInteger
from smnp.token.type import TokenType


# minus -> '-' int
def parseMinus(input, parent):
    if input.isCurrent(TokenType.MINUS):
        token = input.current()
        input.ahead()

        if input.hasCurrent():
            expr = parseInteger(input, parent)

            return IntegerLiteralNode(-expr.value, parent, token.pos)

    return None
