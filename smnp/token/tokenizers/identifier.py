from smnp.token.tools import regexPatternTokenizer
from smnp.token.type import TokenType

def tokenizeIdentifier(input, current, line):
    # TODO: Disallow to create identifiers beggining from a number
    return regexPatternTokenizer(TokenType.IDENTIFIER, r'\w')(input, current, line)
