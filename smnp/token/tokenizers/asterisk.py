from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeAsterisk(input, current, line):
    return tokenizeChar(TokenType.ASTERISK, '*', input, current, line)
