from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.node.percent import PercentNode
from smnp.token.type import TokenType


# int -> INTEGER
def parseInteger(input, parent):
    if input.isCurrent(TokenType.INTEGER):
        integer = IntegerLiteralNode(int(input.current().value), parent, input.current().pos)
        input.ahead()

        return integer
    return None


# percent -> int '%'
# int -> int
def parseIntegerAndPercent(input, parent):
    integer = parseInteger(input, parent)
    if integer is not None and input.isCurrent(TokenType.PERCENT):
        percent = PercentNode(integer, parent, input.current().pos)
        integer.parent = percent
        input.ahead()

        return percent
    return integer