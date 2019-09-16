from enum import Enum


class TokenType(Enum):
    RELATION = '==, !=, >=, <='
    DOUBLE_ASTERISK = '**'
    OPEN_CURLY = '{'
    CLOSE_CURLY = '}'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    OPEN_SQUARE = '['
    CLOSE_SQUARE = ']'
    OPEN_ANGLE = '<'
    CLOSE_ANGLE = '>'
    SEMICOLON = ';'
    ASTERISK = '*'
    PERCENT = '%'
    ASSIGN = '='
    ARROW = '->'
    COMMA = ','
    SLASH = '/'
    MINUS = '-'
    PLUS = '+'
    CARET = '^'
    DOTS = '...'
    AMP = '&'
    DOT = '.'
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    INTEGER = 'integer'
    STRING = 'string'
    FLOAT = 'float'
    NOTE = 'note'
    BOOL = 'bool'
    TYPE = 'type'
    FUNCTION = 'function'
    RETURN = 'return'
    EXTEND = 'extend'
    IMPORT = 'import'
    THROW = 'throw'
    FROM = 'from'
    WITH = 'with'
    ELSE = 'else'
    IF = 'if'
    AS = 'as'
    IDENTIFIER = 'identifier'
    COMMENT = 'comment'

    @property
    def key(self):
        return self.value

    @key.setter
    def key(self, value):
        raise RuntimeError("Cannot change key of token type")
