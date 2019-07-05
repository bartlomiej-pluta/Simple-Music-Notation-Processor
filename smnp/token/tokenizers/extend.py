from smnp.token.tools import tokenizeKeyword
from smnp.token.type import TokenType


def tokenizeExtend(input, current, line):
    return tokenizeKeyword(TokenType.EXTEND, "extend", input, current, line)