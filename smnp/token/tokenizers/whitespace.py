from smnp.token.tools import regexPatternTokenizer

def tokenizeWhitespaces(input, current, line):    
    return regexPatternTokenizer(None, r'\s')(input, current, line)
