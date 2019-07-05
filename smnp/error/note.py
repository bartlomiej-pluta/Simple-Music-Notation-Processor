class NoteException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    def _title(self):
        return "Note Error"