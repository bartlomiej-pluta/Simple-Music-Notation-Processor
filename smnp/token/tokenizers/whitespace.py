from smnp.token.tools import tokenizeRegexPattern

def tokenizeWhitespaces(input, current, line):    
    return tokenizeRegexPattern(None, r'\s', input, current, line)
