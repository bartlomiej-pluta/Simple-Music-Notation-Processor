from smnp.token.tools import tokenizeRegexPattern
from smnp.token.type import TokenType

def tokenizeInteger(input, current, line):    
    return tokenizeRegexPattern(TokenType.INTEGER, r'\d', input, current, line)
