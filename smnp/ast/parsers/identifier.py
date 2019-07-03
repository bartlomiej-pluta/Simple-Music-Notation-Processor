from smnp.ast.node.assignment import AssignmentNode
from smnp.ast.node.function import FunctionCallNode
from smnp.ast.node.identifier import IdentifierNode
from smnp.ast.parsers.expression import parseExpression
from smnp.ast.parsers.list import parseList
from smnp.token.type import TokenType


# id -> IDENTIFIER
def parseIdentifier(input, parent):
    if input.current().type == TokenType.IDENTIFIER:
        identifier = IdentifierNode(input.current().value, parent, input.current().pos)
        input.ahead()

        return identifier
    return None


# identifier -> IDENTIFIER
# functionCall -> identifier list
# assignment -> identifier '=' expr
def parseIdentifierOrFunctionCallOrAssignment(input, parent):
    identifier = parseIdentifier(input, parent)

    # assignment -> identifier '=' expr
    if identifier is not None and input.hasCurrent():
        if input.current().type == TokenType.ASSIGN:
            token = input.current()
            input.ahead()

            expr = parseExpression(input, parent)

            assignment = AssignmentNode(identifier, expr, parent, token.pos)
            identifier.parent = assignment
            expr.parent = assignment

            return assignment

        # functionCall -> identifier list
        args = parseList(input, parent)
        if args is not None:
            functionCall = FunctionCallNode(identifier, args, parent, identifier.pos)
            args.parent = functionCall
            identifier.parent = functionCall
            return functionCall

    return identifier