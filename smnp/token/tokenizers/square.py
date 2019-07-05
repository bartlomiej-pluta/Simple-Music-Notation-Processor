from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeOpenSquare(input, current, line):
    return tokenizeChar(TokenType.OPEN_SQUARE, '[', input, current, line)

def tokenizeCloseSquare(input, current, line):
    return tokenizeChar(TokenType.CLOSE_SQUARE, ']', input, current, line)
