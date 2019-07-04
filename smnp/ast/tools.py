from smnp.ast.node.model import Node
from smnp.error.syntax import SyntaxException


def rollup(parser):
    def _rollup(input, parent):
        node = Node(None, (-1, -1))
        elem = parser(input, node)
        while elem is not None:
            node.append(elem)
            elem = parser(input, node)
        return node.children[0] if len(node.children) > 0 else None
    return _rollup


def assertToken(expected, input):    
    if not input.hasCurrent():
        raise SyntaxException(f"Expected '{expected}'")
    if expected != input.current().type:
        raise SyntaxException(f"Expected '{expected}', found '{input.current().value}'", input.current().pos)


def combineParsers(parsers):
    def combinedParser(input, parent):
        for parser in parsers:
            value = parser(input, parent)
            if value is not None:
                return value
        return None
    return combinedParser
