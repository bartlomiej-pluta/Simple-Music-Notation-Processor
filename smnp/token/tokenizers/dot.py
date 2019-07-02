from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeDot(input, current, line):
    return tokenizeChar(TokenType.DOT, '.', input, current, line)
