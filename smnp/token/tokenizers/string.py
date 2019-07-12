from smnp.token.model import Token
from smnp.token.type import TokenType


def stringTokenizer(input, current, line):
    if input[current] == '"':
        value = input[current]
        char = ''
        consumedChars = 1
        while char != '"':
            if char is None:  # TODO!!!
                print("String not terminated")
            char = input[current + consumedChars]
            value += char
            consumedChars += 1
        return (consumedChars, Token(TokenType.STRING, value[1:len(value)-1], (line, current), value))
    return (0, None)
