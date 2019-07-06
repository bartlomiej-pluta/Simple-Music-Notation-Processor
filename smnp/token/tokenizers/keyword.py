from smnp.token.tools import keywordsTokenizer, separated
from smnp.token.type import TokenType
from smnp.type.model import Type


typeTokenizer = separated(keywordsTokenizer(TokenType.TYPE, *[type.name.lower() for type in Type]))




