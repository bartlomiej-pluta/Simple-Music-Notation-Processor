from enum import Enum
import time
import re
import sys
from Error import SyntaxException

class Tokens:
    def __init__(self, tokens = []):
        self.tokens = tokens
        self.cursor = 0
        self.snap = 0
        
    def append(self, token):
        self.tokens.append(token)
        
    def __getitem__(self, index):
        return self.tokens[index]
    
    def current(self):
        if self.cursor >= len(self.tokens):
            raise RuntimeError(f"Cursor points to not existing token! Cursor = {self.cursor}, len = {len(self.tokens)}")
        return self.tokens[self.cursor]
    
    def next(self, number=1):
        return self.tokens[self.cursor + number]
    
    def prev(self, number=1):
        return self.tokens[self.cursor - number]        
    
    def hasMore(self, count=1):
        return self.cursor + count < len(self.tokens)
    
    def hasCurrent(self):
        return self.cursor < len(self.tokens)
    
    def ahead(self):
        self.cursor += 1        
    
    def snapshot(self):
        self.snapshot = self.cursor
        
    def reset(self):
        self.cursor = self.snapshot
        return self.tokens[self.cursor]
    
    def __str__(self):
        return f"[Cursor: {self.cursor}\n{', '.join([str(token) for token in self.tokens])}]"
    
    def __repr__(self):
        return self.__str__()

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
    MINUS = 15
    FUNCTION = 16
    RETURN = 17    
    DOT = 18

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
    return tokenizeChar(TokenType.OPEN_PAREN, '(', input, current, line)
   
def tokenizeChar(type, char, input, current, line):
    if input[current] == char:
        return (1, Token(type, input[current], (line, current)))
    return (0, None)

def tokenizeCloseParen(input, current, line):
    return tokenizeChar(TokenType.CLOSE_PAREN, ')', input, current, line)

def tokenizeAsterisk(input, current, line):
    return tokenizeChar(TokenType.ASTERISK, '*', input, current, line)

def tokenizeString(input, current, line):
    if input[current] == '"':
        value = input[current]
        char = ''
        consumedChars = 1
        while char != '"':
            if char is None: #TODO!!!
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
    return tokenizeChar(TokenType.COMMA, ',', input, current, line)

def tokenizeInteger(input, current, line):    
    return tokenizeRegexPattern(TokenType.INTEGER, r'\d', input, current, line)

def tokenizeOpenBracket(input, current, line):
    return tokenizeChar(TokenType.OPEN_BRACKET, '{', input, current, line)

def tokenizeCloseBracket(input, current, line):
    return tokenizeChar(TokenType.CLOSE_BRACKET, '}', input, current, line)

def tokenizeAssign(input, current, line):
    return tokenizeChar(TokenType.ASSIGN, '=', input, current, line)

def tokenizeColon(input, current, line):
    return tokenizeChar(TokenType.COLON, ':', input, current, line)

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
                duration = input[current+consumedChars]
                consumedChars += 1
                while current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):
                    duration += input[current+consumedChars]        
                    consumedChars += 1  
                if current+consumedChars < len(input) and input[current+consumedChars] == 'd':
                    duration += input[current+consumedChars]
                    consumedChars += 1
                if len(duration) > 1:
                    value += duration
                else:
                    consumedChars -= 1
            return (consumedChars, Token(TokenType.NOTE, value, (line, current)))
    return (0, None)

def tokenizePercent(input, current, line):
    return tokenizeChar(TokenType.PERCENT, '%', input, current, line)

def tokenizeMinus(input, current, line):
    return tokenizeChar(TokenType.MINUS, '-', input, current, line)

def tokenizeFunction(input, current, line):
    return tokenizeKeyword(TokenType.FUNCTION, 'function', input, current, line)

def tokenizeKeyword(type, keyword, input, current, line):       
    if len(input) >= current+len(keyword) and input[current:current+len(keyword)] == keyword:
        return (len(keyword), Token(type, keyword, (line, current)))
    return (0, None)

def tokenizeReturn(input, current, line):
    return tokenizeKeyword(TokenType.RETURN, 'return', input, current, line)

def tokenizeDot(input, current, line):
    return tokenizeChar(TokenType.DOT, '.', input, current, line)

tokenizers = (
    tokenizeOpenParen, 
    tokenizeCloseParen, 
    tokenizeAsterisk, 
    tokenizeString, 
    tokenizeFunction,
    tokenizeReturn,
    tokenizeInteger,
    tokenizeNote,
    tokenizeIdentifier, 
    tokenizeComma,
    tokenizeOpenBracket,
    tokenizeCloseBracket,
    tokenizeAssign,
    tokenizeColon,    
    tokenizePercent,
    tokenizeMinus,
    tokenizeDot,
    tokenizeComment,
    tokenizeWhitespaces,
)

def doTokenize(lines):    
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
                raise SyntaxException((lineNumber, current), f"Unknown symbol '{line[current]}'")
            
    return [token for token in tokens if token.type is not None]

def tokenize(lines):
    tokens = doTokenize(lines)
    return Tokens([ token for token in tokens if token.type != TokenType.COMMENT])
