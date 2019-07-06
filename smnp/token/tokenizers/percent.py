from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType

def tokenizePercent(input, current, line):
    return charTokenizer(TokenType.PERCENT, '%')(input, current, line)
