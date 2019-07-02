from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizePercent(input, current, line):
    return tokenizeChar(TokenType.PERCENT, '%', input, current, line)
