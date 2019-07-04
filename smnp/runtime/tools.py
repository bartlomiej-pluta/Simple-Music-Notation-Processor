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
