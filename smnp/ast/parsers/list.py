from smnp.ast.node.list import ListNode, ListItemNode, CloseListNode
from smnp.ast.parsers.expression import parseExpression
from smnp.ast.tools import rollup, assertToken
from smnp.token.type import TokenType


# list -> CLOSE_PAREN | expr listTail
def parseList(input, parent):
    if input.current().type == TokenType.OPEN_PAREN:
        node = ListNode(parent, input.current().pos)
        input.ahead()

        # list -> CLOSE_PAREN (end of list)
        if input.hasCurrent() and input.current().type == TokenType.CLOSE_PAREN:
            close = CloseListNode(node, input.current().pos)
            node.append(close)
            input.ahead()
            return node

            # list -> expr listTail
        if input.hasCurrent():
            token = input.current()
            expr = parseExpression(input, node)
            item = ListItemNode(expr, node, token.pos)
            expr.parent = item
            node.append(item)
            listTail = parseListTail(input, item)
            item.append(listTail)
            return node
    return None


# listTail -> COMMA expr listTail | CLOSE_PAREN
def parseListTail(input, parent):
    # listTail -> CLOSE_PAREN
    if input.hasCurrent() and input.current().type == TokenType.CLOSE_PAREN:
        close = CloseListNode(parent, input.current().pos)
        input.ahead()
        return close

    # listTail -> COMMA expr listTail
    if input.hasCurrent() and input.hasMore():
        assertToken(TokenType.COMMA, input)
        input.ahead()
        expr = rollup(parseExpression)(input, parent)
        if expr is not None:
            item = ListItemNode(expr, parent, expr.pos)
            expr.parent = item
            listTail = parseListTail(input, item)
            item.append(listTail)
            listTail.parent = item
            return item

    return None