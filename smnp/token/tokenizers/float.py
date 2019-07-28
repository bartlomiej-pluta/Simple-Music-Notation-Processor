from smnp.token.model import Token
from smnp.token.tools import regexPatternTokenizer, keywordTokenizer, allOf
from smnp.token.type import TokenType


def createToken(pos, beforeDot, dot, afterDot):
    rawValue = f"{beforeDot.value}.{afterDot.value}"
    value = float(rawValue)
    return Token(TokenType.FLOAT, value, pos, rawValue)


floatTokenizer = allOf(
    regexPatternTokenizer(TokenType.INTEGER, r'\d'),
    keywordTokenizer(None, "."),
    regexPatternTokenizer(TokenType.INTEGER, r'\d'),
    createToken=createToken
)
