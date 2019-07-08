def updatePos(exception, node):
    if exception.pos is None:
        exception.pos = node.pos
    return exception