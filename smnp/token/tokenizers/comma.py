from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType


def tokenizeComma(input, current, line):
    return charTokenizer(TokenType.COMMA, ',')(input, current, line)
