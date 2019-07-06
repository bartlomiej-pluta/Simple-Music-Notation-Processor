from smnp.token.tools import regexPatternTokenizer, separate
from smnp.token.type import TokenType

def tokenizeInteger(input, current, line):    
    return separate(regexPatternTokenizer(TokenType.INTEGER, r'\d'))(input, current, line)
