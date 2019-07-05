from smnp.ast.node.block import BlockNode, CloseBlockNode, BlockItemNode
from smnp.ast.parsers.statement import parseStatement
from smnp.token.type import TokenType


def parseBlock(input, parent):
    # '{'
    if input.current().type == TokenType.OPEN_BRACKET:
        token = input.current()
        input.ahead()

        node = BlockNode(parent, token.pos)

        # '}'
        if input.isCurrent(TokenType.CLOSE_BRACKET):
            input.ahead()
            return node

        # blockItem
        if input.hasCurrent():
            item = parseBlockItem(input, node)
            node.append(item)
            return node

    return None


# blockItem -> stmt | '}'
def parseBlockItem(input, parent):
    # '}'
    if input.isCurrent(TokenType.CLOSE_BRACKET):
        close = CloseBlockNode(parent, input.current().pos)
        input.ahead()
        return close

    if input.hasCurrent():
        stmt = parseStatement(input, parent)

        if stmt is not None:
            item = BlockItemNode(stmt, parent, stmt.pos)
            stmt.parent = item
            nextBlockItem = parseBlockItem(input, item)
            if nextBlockItem != None:
                item.append(nextBlockItem)
            return item

    return None