from enum import Enum


class TokenType(Enum):
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    ASTERISK = '*'
    STRING = 'string'
    IDENTIFIER = 'identifier'
    COMMA = ','
    INTEGER = 'integer'
    OPEN_BRACKET = '{'
    CLOSE_BRACKET = '}'
    ASSIGN = '='
    NOTE = 'note'
    COMMENT = 'comment'
    PERCENT = 'percent'
    MINUS = '-'
    FUNCTION = 'function'
    RETURN = 'return'
    DOT = '.'
    OPEN_SQUARE = '['
    CLOSE_SQUARE = ']'
    TYPE = 'type'
    EXTEND = 'extend'
    IMPORT = 'import'
    FROM = 'from'
    AS = 'as'

    @property
    def key(self):
        return self.value

    @key.setter
    def key(self, value):
        raise RuntimeError("Cannot change key of token type")
