from smnp.error.runtime import RuntimeException


class CustomException(RuntimeException):
    def __init__(self, message, pos):
        super().__init__(message, pos)

    def _title(self):
        return "Execution Error"

    def _postMessage(self):
        return "\n" + self.environment.callStackToString() if len(self.environment.callStack) > 0 else ""