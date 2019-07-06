from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType

def tokenizeDot(input, current, line):
    return charTokenizer(TokenType.DOT, '.')(input, current, line)
