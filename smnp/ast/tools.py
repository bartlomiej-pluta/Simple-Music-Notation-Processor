from smnp.error.syntax import SyntaxException


def assertToken(expected, input):
    if not input.hasCurrent():
        raise SyntaxException(f"Expected '{expected}'")
    if expected != input.current().type:
        raise SyntaxException(f"Expected '{expected}', found '{input.current().value}'", input.current().pos)
