from smnp.ast.parsers.statement import parseStatement
from smnp.ast.tools import combineParsers
from smnp.error.syntax import SyntaxException


def parseToken(input, parent):
    value = combineParsers([ parseStatement ])(input, parent)

    if value is None:
        raise SyntaxException(None, "Unknown statement")  # TODO

    return value