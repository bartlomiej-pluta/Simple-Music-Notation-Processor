from smnp.ast.node.program import Program
from smnp.ast.parsers.token import parseToken


def parse(input):
    root = Program()
    while input.hasCurrent():
        root.append(parseToken(input, root))    
    return root


__all__ = ["parse"]