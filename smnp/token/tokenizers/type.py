from smnp.token.tools import tokenizeKeywords
from smnp.token.type import TokenType
from smnp.type.model import Type


def tokenizeType(input, current, line):
    types = [ type.name.lower() for type in Type ]
    return tokenizeKeywords(TokenType.TYPE, input, current, line, *types)