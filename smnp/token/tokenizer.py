from smnp.error.syntax import SyntaxException
from smnp.token.model import TokenList
from smnp.token.tokenizers.bool import boolTokenizer
from smnp.token.tokenizers.comment import commentTokenizer
from smnp.token.tokenizers.identifier import identifierTokenizer
from smnp.token.tokenizers.keyword import typeTokenizer
from smnp.token.tokenizers.note import noteTokenizer
from smnp.token.tokenizers.string import stringTokenizer
from smnp.token.tokenizers.whitespace import whitespacesTokenizer
from smnp.token.tools import defaultTokenizer, separated, regexPatternTokenizer
from smnp.token.type import TokenType

tokenizers = (
    # Characters
    defaultTokenizer(TokenType.OPEN_CURLY),
    defaultTokenizer(TokenType.CLOSE_CURLY),
    defaultTokenizer(TokenType.OPEN_PAREN),
    defaultTokenizer(TokenType.CLOSE_PAREN),
    defaultTokenizer(TokenType.OPEN_SQUARE),
    defaultTokenizer(TokenType.CLOSE_SQUARE),
    defaultTokenizer(TokenType.OPEN_ANGLE),
    defaultTokenizer(TokenType.CLOSE_ANGLE),
    defaultTokenizer(TokenType.DOUBLE_ASTERISK),
    defaultTokenizer(TokenType.ASTERISK),
    defaultTokenizer(TokenType.ASSIGN),
    defaultTokenizer(TokenType.ARROW),
    defaultTokenizer(TokenType.COMMA),
    defaultTokenizer(TokenType.SLASH),
    defaultTokenizer(TokenType.MINUS),
    defaultTokenizer(TokenType.PLUS),
    defaultTokenizer(TokenType.DOTS),
    defaultTokenizer(TokenType.AMP),
    defaultTokenizer(TokenType.DOT),

    # Types
    separated(regexPatternTokenizer(TokenType.INTEGER, r'\d')),
    stringTokenizer,
    noteTokenizer,
    boolTokenizer,
    typeTokenizer,

    # Keywords
    separated(defaultTokenizer(TokenType.FUNCTION)),
    separated(defaultTokenizer(TokenType.RETURN)),
    separated(defaultTokenizer(TokenType.EXTEND)),
    separated(defaultTokenizer(TokenType.IMPORT)),
    separated(defaultTokenizer(TokenType.FROM)),
    separated(defaultTokenizer(TokenType.AS)),

    # Identifier (couldn't be before keywords!)
    identifierTokenizer,

    # Other
    whitespacesTokenizer,
    commentTokenizer,
)

filters = [
    lambda token: token.type is not None,
    lambda token: token.type != TokenType.COMMENT
]


def tokenize(lines):
    tokens = []
    for lineNumber, line in enumerate(lines):
        current = 0
        while current < len(line):
            consumedChars, token = combinedTokenizer(line, current, lineNumber)

            if consumedChars == 0:
                raise SyntaxException(f"Unknown symbol '{line[current]}'", (lineNumber, current))

            current += consumedChars
            tokens.append(token)

    return TokenList(filterTokens(filters, tokens), lines)


def combinedTokenizer(line, current, lineNumber):
    for tokenizer in tokenizers:
        consumedChars, token = tokenizer(line, current, lineNumber)
        if consumedChars > 0:
            return (consumedChars, token)
    return (0, None)


def filterTokens(filters, tokens):
    if not filters:
        return tokens

    return list(filterTokens(filters[1:], (token for token in tokens if filters[0](token))))


__all__ = ["tokenize"]
