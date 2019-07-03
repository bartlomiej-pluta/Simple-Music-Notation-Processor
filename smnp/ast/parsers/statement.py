def parseStatement(input, parent):
    from smnp.ast.tools import combineParsers
    from smnp.ast.parsers.asterisk import parseAsterisk
    from smnp.ast.parsers.block import parseBlock
    from smnp.ast.parsers.expression import parseExpression
    from smnp.ast.parsers.function import parseFunctionDefinition
    from smnp.ast.parsers.ret import parseReturn

    parsers = [
        parseBlock,
        parseFunctionDefinition,
        parseReturn,
        parseExpression,
    ]

    stmt = combineParsers(parsers)(input, parent)

    asterisk = parseAsterisk(stmt, input, parent)
    if asterisk is not None:
        return asterisk

    return stmt