from smnp.error.base import SmnpException


class RuntimeException(SmnpException):
    def __init__(self, msg, pos):
        super().__init__(msg, pos)

    def _title(self):
        return "Runtime Error"

    # def message(self):
    #     posStr = "" if self.pos is None else f" [line {self.pos[0] + 1}, col {self.pos[1] + 1}]"
    #     return f"Runtime error{posStr}:\n{self.mmsg}"
