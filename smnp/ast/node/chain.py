from smnp.ast.node.atom import AtomParser
from smnp.ast.node.operator import BinaryOperator
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Chain(BinaryOperator):
    pass


ChainParser = Parser.leftAssociativeOperatorParser(AtomParser, [TokenType.DOT], AtomParser, lambda left, op, right: Chain.withValues(left, op, right))