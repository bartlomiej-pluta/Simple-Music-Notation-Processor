from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeColon(input, current, line):
    return tokenizeChar(TokenType.COLON, ':', input, current, line)
