from smnp.ast.node.factor import FactorParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.node.valuable import Valuable
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Term(Valuable):
    pass

TermParser = Parser.leftAssociativeOperatorParser(FactorParser, [TokenType.ASTERISK, TokenType.SLASH], FactorParser,
                                                    lambda left, op, right: Term.withValue(BinaryOperator.withValues(left, op, right)))