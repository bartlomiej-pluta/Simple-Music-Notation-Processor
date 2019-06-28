from enum import Enum
import time
import re
import sys

class TokenType(Enum):
    OPEN_PAREN = 1
    CLOSE_PAREN = 2
    ASTERISK = 3
    STRING = 4
    IDENTIFIER = 5
    COMMA = 6
    INTEGER = 7
    OPEN_BRACKET = 8
    CLOSE_BRACKET = 9
    ASSIGN = 10
    COLON = 11
    NOTE = 12
    COMMENT = 13
    PERCENT = 14
    
class TokenizerError(Exception):
    pass
    

class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value    
        self.pos = pos
    def __str__(self):
        return "Token(" + str(self.type) + ", '" + self.value + "', " + str(self.pos) + ")"
    def __repr__(self):
        return self.__str__()

def tokenizeOpenParen(input, current, line):
    if input[current] == '(':
        return (1, Token(TokenType.OPEN_PAREN, input[current], (line, current)))
    return (0, None)

def tokenizeCloseParen(input, current, line):
    if input[current] == ')':
        return (1, Token(TokenType.CLOSE_PAREN, input[current], (line, current)))
    return (0, None)

def tokenizeAsterisk(input, current, line):
    if input[current] == '*':
        return (1, Token(TokenType.ASTERISK, input[current], (line, current)))
    return (0, None)

def tokenizeString(input, current, line):
    if input[current] == '"':
        value = input[current]
        char = ''
        consumedChars = 1
        while char != '"':
            if char is None:
                print("String not terminated")
            char = input[current + consumedChars]
            value += char
            consumedChars += 1
        return (consumedChars, Token(TokenType.STRING, value, (line, current)))
    return (0, None)

def tokenizeRegexPattern(type, pattern, input, current, line):    
    consumedChars = 0
    value = ''
    
    while current+consumedChars < len(input) and re.match(pattern, input[current+consumedChars]):
        value += input[current+consumedChars]        
        consumedChars += 1            
    return (consumedChars, Token(type, value, (line, current)) if consumedChars > 0 else None)
        
def tokenizeWhitespaces(input, current, line):    
    return tokenizeRegexPattern(None, r'\s', input, current, line)

def tokenizeIdentifier(input, current, line):
    return tokenizeRegexPattern(TokenType.IDENTIFIER, r'\w', input, current, line)

def tokenizeComma(input, current, line):
    if input[current] == ',':
        return (1, Token(TokenType.COMMA, input[current], (line, current)))
    return (0, None)

def tokenizeInteger(input, current, line):    
    return tokenizeRegexPattern(TokenType.INTEGER, r'\d', input, current, line)

def tokenizeOpenBracket(input, current, line):
    if input[current] == '{':
        return (1, Token(TokenType.OPEN_BRACKET, input[current], (line, current)))
    return (0, None)

def tokenizeCloseBracket(input, current, line):
    if input[current] == '}':
        return (1, Token(TokenType.CLOSE_BRACKET, input[current], (line, current)))
    return (0, None)

def tokenizeAssign(input, current, line):
    if input[current] == '=':
        return (1, Token(TokenType.ASSIGN, input[current], (line, current)))
    return (0, None)

def tokenizeColon(input, current, line):
    if input[current] == ':':
        return (1, Token(TokenType.COLON, input[current], (line, current)))
    return (0, None)

def tokenizeComment(input, current, line):
    if input[current] == '#':
        consumedChars = 0
        value = ''
        while current+consumedChars < len(input):
            value += input[current+consumedChars]
            consumedChars += 1            
            pass
        return (consumedChars, Token(TokenType.COMMENT, value, (line, current)))
    return (0, None)

def tokenizeNote(input, current, line):
    consumedChars = 0
    value = ''
    if input[current] == '@':
        consumedChars += 1
        value += input[current]
        if input[current+consumedChars] in ('C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'A', 'a', 'H', 'h', 'B', 'b'):
            value += input[current+consumedChars]
            consumedChars += 1
            
            if current+consumedChars < len(input) and input[current+consumedChars] in ('b', '#'):                        
                value += input[current+consumedChars]
                consumedChars += 1
                
            if current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):            
                value += input[current+consumedChars]
                consumedChars += 1
                
            if current+consumedChars < len(input) and input[current+consumedChars] == '.':            
                value += input[current+consumedChars]
                consumedChars += 1
                while current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):
                    value += input[current+consumedChars]        
                    consumedChars += 1  
            return (consumedChars, Token(TokenType.NOTE, value, (line, current)))
    return (0, None)

def tokenizePercent(input, current, line):
    if input[current] == '%':
        return (1, Token(TokenType.PERCENT, input[current], (line, current)))
    return (0, None)

tokenizers = (
    tokenizeOpenParen, 
    tokenizeCloseParen, 
    tokenizeAsterisk, 
    tokenizeString, 
    tokenizeInteger,
    tokenizeNote,
    tokenizeIdentifier, 
    tokenizeComma,
    tokenizeOpenBracket,
    tokenizeCloseBracket,
    tokenizeAssign,
    tokenizeColon,
    tokenizePercent,
    tokenizeComment,
    tokenizeWhitespaces
)

def tokenize(lines):    
    tokens = []         
    for lineNumber, line in enumerate(lines):    
        current = 0
        while current < len(line):
            tokenized = False
            for tokenizer in tokenizers:
                consumedChars, value = tokenizer(line, current, lineNumber)
                if consumedChars > 0:
                    tokens.append(value)
                    current += consumedChars
                    tokenized = True
                    break            
            
            if not tokenized:
                raise TokenizerError(f"Line {lineNumber+1}, col {current+1}: unknown symbol '{line[current]}'")
            
    return [token for token in tokens if token.type is not None]

if __name__ == "__main__":   
    try:
        with open(sys.argv[1], 'r') as source:
            lines = [line.rstrip('\n') for line in source.readlines()]
            
            tokens = tokenize(lines)    
        
        for token in tokens:
            print(token)        
    except TokenizerError as e:
        print(str(e))
    
