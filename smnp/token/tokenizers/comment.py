from smnp.token.type import TokenType
from smnp.token.model import Token

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
