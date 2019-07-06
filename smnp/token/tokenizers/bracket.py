from smnp.token.tools import charTokenizer
from smnp.token.type import TokenType


def tokenizeOpenBracket(input, current, line):
    return charTokenizer(TokenType.OPEN_BRACKET, '{')(input, current, line)


def tokenizeCloseBracket(input, current, line):
    return charTokenizer(TokenType.CLOSE_BRACKET, '}')(input, current, line)
