import re

from smnp.token.model import Token


def tokenizeChar(type, char, input, current, line):
    if input[current] == char:
        return (1, Token(type, input[current], (line, current)))
    return (0, None)

def tokenizeRegexPattern(type, pattern, input, current, line):    
    consumedChars = 0
    value = ''
    
    while current+consumedChars < len(input) and re.match(pattern, input[current+consumedChars]):
        value += input[current+consumedChars]        
        consumedChars += 1            
    return (consumedChars, Token(type, value, (line, current)) if consumedChars > 0 else None)

def tokenizeKeywords(type, input, current, line, *keywords):
    for keyword in keywords:
        result = tokenizeKeyword(type, keyword, input, current, line)
        if result[0] > 0:
            return result
    return (0, None)

def tokenizeKeyword(type, keyword, input, current, line):       
    if len(input) >= current+len(keyword) and input[current:current+len(keyword)] == keyword:
        return (len(keyword), Token(type, keyword, (line, current)))
    return (0, None)
