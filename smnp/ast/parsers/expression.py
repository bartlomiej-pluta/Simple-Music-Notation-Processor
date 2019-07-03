def parseExpression(input, parent):
    from smnp.ast.tools import combineParsers
    from smnp.ast.parsers.access import parseAccess
    from smnp.ast.parsers.colon import parseColon
    from smnp.ast.parsers.identifier import parseIdentifierOrFunctionCallOrAssignment
    from smnp.ast.parsers.integer import parseIntegerAndPercent
    from smnp.ast.parsers.list import parseList
    from smnp.ast.parsers.minus import parseMinus
    from smnp.ast.parsers.note import parseNote
    from smnp.ast.parsers.string import parseString

    parsers = [
        parseIntegerAndPercent,
        parseMinus,
        parseString,
        parseNote,
        parseList,
        parseIdentifierOrFunctionCallOrAssignment,
        parseAccess,
    ]

    expr = combineParsers(parsers)(input, parent)

    colon = parseColon(expr, input, parent)
    if colon is not None:
        return colon

    return expr