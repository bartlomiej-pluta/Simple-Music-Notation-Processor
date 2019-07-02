import re
from smnp.token.type import TokenType
from smnp.token.model import Token

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
