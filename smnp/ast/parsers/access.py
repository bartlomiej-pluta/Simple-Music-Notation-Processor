from smnp.ast.node.access import AccessNode
from smnp.ast.parsers.expression import parseExpression
from smnp.token.type import TokenType


# access -> expr '.' expr
# TODO: dodać dziedziczenie wszystkich expressions po jednym typie ExpressionNode
# i potem sprawdzać przy wszystkich parent.pop(-1) czy pobrany z parenta element
# jest rzeczywiście wyrażeniem, bo teraz możliwe jest np. {}.fun()
def parseAccess(input, parent):
    if input.isCurrent(TokenType.DOT):
        token = input.current()
        input.ahead()

        element = parent.pop(-1)

        property = parseExpression(input, parent)

        node = AccessNode(element, property, parent, token.pos)
        element.parent = node
        property.parent = node

        return node
    return None