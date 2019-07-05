def flatListNode(listNode):
    if len(listNode.children[0].children) == 1:
        return []
    return _flatListNode(listNode.children[0], [])


def _flatListNode(listItemNode, list = []):
    if len(listItemNode.children) == 2:
        value = listItemNode.children[0]
        next = listItemNode.children[1]
        list.append(value)
        _flatListNode(next, list)
    return list



    # NEW AST
    # def toFlatList(parser):
    #     def decoratedParser(input):
    #         result = parser(input)
    #
    #         if result.result:
    #             value = flattenList(result.node)
    #             node = iterableNodeType()
    #             for v in value:
    #                 node.append(v)
    #             return ParseResult.OK(node)
    #
    #         return ParseResult.FAIL()
    #
    #     return decoratedParser
    #
    #
    # def flattenList(node, output=None):
    #     if output is None:
    #         output = []
    #
    #     if type(node.value) != IgnoredNode:
    #         output.append(node.value)
    #
    #     if type(node.next) != IgnoredNode:
    #         flattenList(node.next, output)
    #
    #     return output