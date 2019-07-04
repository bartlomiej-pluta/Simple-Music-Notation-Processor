from smnp.error.base import SmnpException


class NoteException(SmnpException):
    def __init__(self, msg):
        super().__init__(msg)

    def _title(self):
        return "Note Error"