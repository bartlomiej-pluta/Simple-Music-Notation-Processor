from smnp.token.tools import keywordsTokenizer, separated
from smnp.token.type import TokenType


def boolTokenizer(input, current, line):
    consumedChars, token = separated(keywordsTokenizer(TokenType.BOOL, "true", "false"))(input, current, line)
    if consumedChars > 0:
        token.value = token.value == "true"
        return (consumedChars, token)

    return (0, None)
