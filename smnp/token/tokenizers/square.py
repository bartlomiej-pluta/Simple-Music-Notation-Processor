from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType

def tokenizeOpenSquare(input, current, line):
    return charTokenizer(TokenType.OPEN_SQUARE, '[')(input, current, line)

def tokenizeCloseSquare(input, current, line):
    return charTokenizer(TokenType.CLOSE_SQUARE, ']')(input, current, line)
