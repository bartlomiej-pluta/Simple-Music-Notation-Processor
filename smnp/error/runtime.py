from smnp.error.base import SmnpException


class RuntimeException(SmnpException):
    def __init__(self, msg, pos, environment=None):
        super().__init__(msg, pos)
        self.environment = environment

    def _title(self):
        return "Runtime Error"

    def _postMessage(self):
        return "\n" + self.environment.callStackToString() if len(self.environment.callStack) > 0 else ""

    # def message(self):
    #     posStr = "" if self.pos is None else f" [line {self.pos[0] + 1}, col {self.pos[1] + 1}]"
    #     return f"Runtime error{posStr}:\n{self.mmsg}"
