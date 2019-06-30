from enum import Enum
from Error import ParseError
import math

class NotePitch(Enum):
    C = 1
    CIS = 2
    D = 3
    DIS = 4
    E = 5
    F = 6
    FIS = 7
    G = 8
    GIS = 9
    A = 10
    AIS = 11
    H = 12
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()    
    
    def toFrequency(self):
        return {
            NotePitch.C: 16.35,
            NotePitch.CIS: 17.32,
            NotePitch.D: 18.35,
            NotePitch.DIS: 19.45,
            NotePitch.E: 20.60,
            NotePitch.F: 21.83,
            NotePitch.FIS: 23.12,
            NotePitch.G: 24.50,
            NotePitch.GIS: 25.96,
            NotePitch.A: 27.50,
            NotePitch.AIS: 29.17,
            NotePitch.H: 30.87
        }[self]
    
    @staticmethod
    def checkInterval(a, b):
        return a.value - b.value
    
    @staticmethod
    def toPitch(string):
        try:
            map = { 'c': NotePitch.C, 'c#': NotePitch.CIS, 'db': NotePitch.CIS, 'd': NotePitch.D,
                'd#': NotePitch.DIS, 'eb': NotePitch.DIS, 'e': NotePitch.E, 'fb': NotePitch.E, 'e#': NotePitch.F,
                'f': NotePitch.F, 'f#': NotePitch.FIS, 'gb': NotePitch.FIS, 'g': NotePitch.G, 'g#': NotePitch.GIS,
                'ab': NotePitch.GIS, 'a': NotePitch.A, 'a#': NotePitch.AIS, 'b': NotePitch.AIS, 'h': NotePitch.H
                }
            return map[string.lower()]
        except KeyError as e:
            raise ParseError(f"Note '{string}' does not exist")
    
    @staticmethod
    def range(a, b):
        aValue = a.value
        bValue = b.value
        
        return [note[1] for note in NotePitch.__members__.items() if note[1].value >= aValue and note[1].value <= bValue]

class Note:
    def __init__(self, note, octave = 4, duration = 4):        
        if type(note) == str:            
            self.note = NotePitch.toPitch(note)
        else:
            self.note = note
        self.octave = octave
        self.duration = duration        
    
    def hash(self):
        return f"{self.note.value}{self.octave}{self.duration}"
    
    def toFrequency(self):
        return self.note.toFrequency() * 2 ** self.octave
    
    def transpose(self, interval):
        origIntRepr = self._intRepr()
        transposedIntRepr = origIntRepr + interval
        pitch = transposedIntRepr % len(NotePitch)
        note = NotePitch(pitch if pitch != 0 else self.note.value)
        octave = int(transposedIntRepr / len(NotePitch))
        return Note(note, octave, self.duration)
    
    def _intRepr(self):
        return self.octave * len(NotePitch) + self.note.value
    
    def __str__(self):
        return f"{self.note}({self.octave}')[{self.duration}]"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def checkInterval(a, b):
        return a._intRepr() - b._intRepr()
    
    @staticmethod
    def range(a, b):        
        return [Note(note, 1, 1) for note in NotePitch.range(a.note, b.note)]
    
def intervalToString(interval):
    octaveInterval = int(abs(interval) / len(NotePitch))
    pitchInterval = abs(interval) % len(NotePitch)
    pitchIntervalName = {
        0: "1",
        1: "1>/2<",
        2: "2",
        3: "3<",
        4: "3>",
        5: "4",
        6: "4>/5<",
        7: "5",
        8: "6<",
        9: "6>",
        10: "7<",
        11: "7>"        
    }
    return (str(pitchIntervalName[pitchInterval]) + (f"(+{octaveInterval}')" if octaveInterval > 0 else ""))
