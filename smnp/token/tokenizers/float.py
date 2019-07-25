from smnp.token.model import Token
from smnp.token.tools import regexPatternTokenizer, keywordTokenizer
from smnp.token.type import TokenType


def floatTokenizer(input, current, line):
    consumedChars = 0
    value = ""
    consumed, token = regexPatternTokenizer(TokenType.INTEGER, r'\d')(input, current, line)
    if consumed > 0:
        consumedChars += consumed
        value += token.value
        consumed, token = keywordTokenizer(TokenType.DOT, ".")(input, current+consumedChars, line)
        if consumed > 0:
            consumedChars += consumed
            value += token.value
            consumed, token = regexPatternTokenizer(TokenType.INTEGER, r'\d')(input, current+consumedChars, line)
            if consumed > 0:
                consumedChars += consumed
                value += token.value
                print(value)
                return (consumedChars, Token(TokenType.FLOAT, float(value), (current, line), value))


    return (0, None)