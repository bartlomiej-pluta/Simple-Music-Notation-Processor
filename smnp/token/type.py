from enum import Enum


class TokenType(Enum):
    OPEN_CURLY = '{'
    CLOSE_CURLY = '}'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    OPEN_SQUARE = '['
    CLOSE_SQUARE = ']'
    OPEN_ANGLE = '<'
    CLOSE_ANGLE = '>'
    ASTERISK = '*'
    ASSIGN = '='
    COMMA = ','
    MINUS = '-'
    DOT = '.'
    INTEGER = 'integer'
    STRING = 'string'
    NOTE = 'note'
    TYPE = 'type'
    FUNCTION = 'function'
    RETURN = 'return'
    EXTEND = 'extend'
    IMPORT = 'import'
    FROM = 'from'
    AS = 'as'
    IDENTIFIER = 'identifier'
    COMMENT = 'comment'
    PERCENT = 'percent'

    @property
    def key(self):
        return self.value

    @key.setter
    def key(self, value):
        raise RuntimeError("Cannot change key of token type")
