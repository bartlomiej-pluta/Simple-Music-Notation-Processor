from smnp.ast.node.chain import ChainParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Factor(BinaryOperator):
    pass


FactorParser = Parser.leftAssociativeOperatorParser(ChainParser, [TokenType.DOUBLE_ASTERISK], ChainParser, lambda left, op, right: Factor.withValues(left, op, right))