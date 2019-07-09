import sounddevice as sd
import soundfile as sf


class Sound:
    def __init__(self, file):
        self.file = file
        self.data, self.fs = sf.read(file, dtype='float32')

    def play(self):
        sd.play(self.data, self.fs, blocking=True)

    def __str__(self):
        return f"sound[{self.file}]"

    def __repr__(self):
        return self.__str__()