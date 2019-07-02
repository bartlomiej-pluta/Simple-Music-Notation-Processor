from smnp.token.tools import tokenizeKeyword
from smnp.token.type import TokenType

def tokenizeReturn(input, current, line):
    return tokenizeKeyword(TokenType.RETURN, 'return', input, current, line)
