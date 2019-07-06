from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType


def tokenizeOpenParen(input, current, line):
    return charTokenizer(TokenType.OPEN_PAREN, '(')(input, current, line)

def tokenizeCloseParen(input, current, line):
    return charTokenizer(TokenType.CLOSE_PAREN, ')')(input, current, line)
