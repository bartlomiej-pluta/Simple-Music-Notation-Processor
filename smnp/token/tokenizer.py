from smnp.error.syntax import SyntaxException
from smnp.token.model import TokenList
from smnp.token.tokenizers.assign import tokenizeAssign
from smnp.token.tokenizers.asterisk import tokenizeAsterisk
from smnp.token.tokenizers.bracket import tokenizeOpenBracket, tokenizeCloseBracket
from smnp.token.tokenizers.comma import tokenizeComma
from smnp.token.tokenizers.comment import tokenizeComment
from smnp.token.tokenizers.dot import tokenizeDot
from smnp.token.tokenizers.identifier import tokenizeIdentifier
from smnp.token.tokenizers.integer import tokenizeInteger
from smnp.token.tokenizers.keyword import tokenizeType, tokenizeFunction, tokenizeReturn, tokenizeExtend, \
    tokenizeImport, tokenizeFrom, tokenizeAs
from smnp.token.tokenizers.minus import tokenizeMinus
from smnp.token.tokenizers.note import tokenizeNote
from smnp.token.tokenizers.paren import tokenizeOpenParen, tokenizeCloseParen
from smnp.token.tokenizers.percent import tokenizePercent
from smnp.token.tokenizers.square import tokenizeOpenSquare, tokenizeCloseSquare
from smnp.token.tokenizers.string import tokenizeString
from smnp.token.tokenizers.whitespace import tokenizeWhitespaces
from smnp.token.type import TokenType

tokenizers = (
    tokenizeOpenParen, 
    tokenizeCloseParen,
    tokenizeOpenSquare,
    tokenizeCloseSquare,
    tokenizeAsterisk,
    tokenizeType,
    tokenizeString, 
    tokenizeFunction,
    tokenizeReturn,
    tokenizeExtend,
    tokenizeImport,
    tokenizeFrom,
    tokenizeAs,
    tokenizeInteger,
    tokenizeNote,
    tokenizeIdentifier, 
    tokenizeComma,
    tokenizeOpenBracket,
    tokenizeCloseBracket,
    tokenizeAssign,
    tokenizePercent,
    tokenizeMinus,
    tokenizeDot,
    tokenizeComment,
    tokenizeWhitespaces,
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
            
    return TokenList(filterTokens(filters, tokens))


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
