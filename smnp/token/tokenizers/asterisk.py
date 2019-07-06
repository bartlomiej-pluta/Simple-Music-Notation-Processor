from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType


def tokenizeAsterisk(input, current, line):
    return charTokenizer(TokenType.ASTERISK, '*')(input, current, line)
