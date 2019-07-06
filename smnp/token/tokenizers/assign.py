from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType

def tokenizeAssign(input, current, line):
    return charTokenizer(TokenType.ASSIGN, '=')(input, current, line)
