from smnp.error.base import SmnpException


class IllegalFunctionInvocationException(SmnpException):
    def __init__(self, expected, found):
        self.msg = f"Illegal function invocation\n\nExpected signature:\n{expected}\n\nFound:\n{found}"