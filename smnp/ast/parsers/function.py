from smnp.ast.node.function import FunctionDefinitionNode
from smnp.ast.parsers.block import parseBlock
from smnp.ast.parsers.identifier import parseIdentifier
from smnp.ast.parsers.list import parseList
from smnp.ast.tools import assertToken
from smnp.token.type import TokenType


def parseFunctionDefinition(input, parent):
    if input.isCurrent(TokenType.FUNCTION):
        token = input.current()
        input.ahead()

        assertToken(TokenType.IDENTIFIER, input)
        identifier = parseIdentifier(input, parent)

        assertToken(TokenType.OPEN_PAREN, input)
        args = parseList(input, parent)

        assertToken(TokenType.OPEN_BRACKET, input)
        body = parseBlock(input, parent)

        function = FunctionDefinitionNode(identifier, args, body, parent, token.pos)
        identifier.parent = function
        args.parent = function
        body.parent = function

        return function
    return None