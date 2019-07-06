from smnp.token.tools import keywordsTokenizer, keywordTokenizer, separate
from smnp.token.type import TokenType
from smnp.type.model import Type


def tokenizeType(input, current, line):
    types = [ type.name.lower() for type in Type ]
    return separate(keywordsTokenizer(TokenType.TYPE, *types))(input, current, line)


def tokenizeReturn(input, current, line):
    return separate(keywordTokenizer(TokenType.RETURN, 'return'))(input, current, line)


def tokenizeFunction(input, current, line):
    return separate(keywordTokenizer(TokenType.FUNCTION, 'function'))(input, current, line)


def tokenizeExtend(input, current, line):
    return separate(keywordTokenizer(TokenType.EXTEND, "extend"))(input, current, line)


def tokenizeImport(input, current, line):
    return separate(keywordTokenizer(TokenType.IMPORT, "import"))(input, current, line)


def tokenizeFrom(input, current, line):
    return separate(keywordTokenizer(TokenType.FROM, "from"))(input, current, line)


def tokenizeAs(input, current, line):
    return separate(keywordTokenizer(TokenType.AS, "as"))(input, current, line)


