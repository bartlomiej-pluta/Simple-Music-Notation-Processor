from smnp.token.tools import tokenizeChar
from smnp.token.type import TokenType

def tokenizeOpenBracket(input, current, line):
    return tokenizeChar(TokenType.OPEN_BRACKET, '{', input, current, line)

def tokenizeCloseBracket(input, current, line):
    return tokenizeChar(TokenType.CLOSE_BRACKET, '}', input, current, line)
