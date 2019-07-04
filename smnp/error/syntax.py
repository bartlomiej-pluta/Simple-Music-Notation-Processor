from smnp.error.base import SmnpException


class SyntaxException(SmnpException):
    def __init__(self, msg, pos=None):
        super().__init__(msg, pos)

    def _title(self):
        return "Syntax Error"

