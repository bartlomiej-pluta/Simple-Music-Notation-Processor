from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeOpenParen(input, current, line):
    return tokenizeChar(TokenType.OPEN_PAREN, '(', input, current, line)

def tokenizeCloseParen(input, current, line):
    return tokenizeChar(TokenType.CLOSE_PAREN, ')', input, current, line)
