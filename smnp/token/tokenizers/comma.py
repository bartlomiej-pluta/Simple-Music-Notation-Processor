from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeComma(input, current, line):
    return tokenizeChar(TokenType.COMMA, ',', input, current, line)
