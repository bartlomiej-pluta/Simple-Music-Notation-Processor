from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeMinus(input, current, line):
    return tokenizeChar(TokenType.MINUS, '-', input, current, line)
