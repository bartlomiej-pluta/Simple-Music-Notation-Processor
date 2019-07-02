from smnp.token.tools import tokenizeRegexPattern
from smnp.token.type import TokenType

def tokenizeIdentifier(input, current, line):
    return tokenizeRegexPattern(TokenType.IDENTIFIER, r'\w', input, current, line)
