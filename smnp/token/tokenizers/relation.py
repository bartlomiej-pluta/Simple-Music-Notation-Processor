from smnp.token.tools import keywordsTokenizer
from smnp.token.type import TokenType


def relationOperatorTokenizer(input, current, line):
    return keywordsTokenizer(TokenType.RELATION, "==", "!=", ">=", "<=", ">", "<")(input, current, line)