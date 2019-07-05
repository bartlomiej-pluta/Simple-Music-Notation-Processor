from smnp.ast.node.string import StringLiteralNode
from smnp.token.type import TokenType


# string -> STRING
def parseString(input, parent):
    if input.isCurrent(TokenType.STRING):
        string = StringLiteralNode(input.current().value[1:len(input.current().value) - 1], parent, input.current().pos)
        input.ahead()

        return string
    return None