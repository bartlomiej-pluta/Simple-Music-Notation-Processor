from smnp.token.tools import tokenizeKeywords, tokenizeKeyword
from smnp.token.type import TokenType
from smnp.type.model import Type


def tokenizeType(input, current, line):
    types = [ type.name.lower() for type in Type ]
    return tokenizeKeywords(TokenType.TYPE, input, current, line, *types)


def tokenizeReturn(input, current, line):
    return tokenizeKeyword(TokenType.RETURN, 'return', input, current, line)


def tokenizeFunction(input, current, line):
    return tokenizeKeyword(TokenType.FUNCTION, 'function', input, current, line)


def tokenizeExtend(input, current, line):
    return tokenizeKeyword(TokenType.EXTEND, "extend", input, current, line)


def tokenizeImport(input, current, line):
    return tokenizeKeyword(TokenType.IMPORT, "import", input, current, line)


def tokenizeFrom(input, current, line):
    return tokenizeKeyword(TokenType.FROM, "from", input, current, line)


def tokenizeAs(input, current, line):
    return tokenizeKeyword(TokenType.AS, "as", input, current, line)


