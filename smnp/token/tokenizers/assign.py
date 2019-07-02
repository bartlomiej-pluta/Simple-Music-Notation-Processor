from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeAssign(input, current, line):
    return tokenizeChar(TokenType.ASSIGN, '=', input, current, line)
