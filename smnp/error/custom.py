from smnp.error.base import SmnpException


class CustomException(SmnpException):
    def __init__(self, message, pos):
        super().__init__(message, pos)

    def _title(self):
        return "Execution Error"
