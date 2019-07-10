from smnp.error.runtime import RuntimeException


class IllegalFunctionInvocationException(RuntimeException):
    def __init__(self, expected, found, pos=None):
        super().__init__(f"Expected signature:\n{expected}\n\nFound:\n{found}", pos)

    def _title(self):
        return "Invocation Error"


class FunctionNotFoundException(RuntimeException):
    def __init__(self, function, pos=None):
        super().__init__(f"Function '{function}' not found", pos)

    def _title(self):
        return "Invocation Error"


class MethodNotFoundException(RuntimeException):
    def __init__(self, object, method, pos=None):
        super().__init__(f"Method '{method}' of type '{object}' not found", pos)

    def _title(self):
        return "Invocation Error"


class IllegalArgumentException(RuntimeException):
    def __init__(self, msg, pos=None):
        super().__init__(msg, pos)

    def _title(self):
        return "Argument Error"