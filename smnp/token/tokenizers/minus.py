from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType

def tokenizeMinus(input, current, line):
    return charTokenizer(TokenType.MINUS, '-')(input, current, line)
