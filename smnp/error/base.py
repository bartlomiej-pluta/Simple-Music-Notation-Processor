class SmnpException(Exception):
    def __init__(self, msg, pos):
        self.msg = msg
        self.pos = pos
        self.file = None

    def _title(self):
        pass

    def _postMessage(self):
        return ""

    def _position(self):
        return "" if self.pos is None else f"[line {self.pos[0]+1}, col {self.pos[1]+1}]"

    def _file(self):
        return "" if self.file is None else f"File: {self.file}"

    def message(self):
        return f"{self._title()}\n{self._file()} {self._position()}\n\n{self.msg}\n{self._postMessage()}"
