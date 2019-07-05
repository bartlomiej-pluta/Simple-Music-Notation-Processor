from enum import Enum

class TokenType(Enum):
    OPEN_PAREN = 1
    CLOSE_PAREN = 2
    ASTERISK = 3
    STRING = 4
    IDENTIFIER = 5
    COMMA = 6
    INTEGER = 7
    OPEN_BRACKET = 8
    CLOSE_BRACKET = 9
    ASSIGN = 10
    COLON = 11
    NOTE = 12
    COMMENT = 13
    PERCENT = 14
    MINUS = 15
    FUNCTION = 16
    RETURN = 17    
    DOT = 18
    OPEN_SQUARE = 19
    CLOSE_SQUARE = 20
