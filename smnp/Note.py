from enum import Enum
import math
from Error import SyntaxException

class NotePitch(Enum):
    C = 0
    CIS = 1
    D = 2
    DIS = 3
    E = 4
    F = 5
    FIS = 6
    G = 7
    GIS = 8
    A = 9
    AIS = 10
    H = 11
    
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
            raise SyntaxException(None, f"Note '{string}' does not exist")

class Note:
    def __init__(self, note, octave = 4, duration = 4, dot = False):        
        if type(note) == str:            
            self.note = NotePitch.toPitch(note)
        else:
            self.note = note
        self.octave = octave
        self.duration = duration    
        self.dot = dot        
    
    def toFrequency(self):
        return self.note.toFrequency() * 2 ** self.octave
    
    def transpose(self, interval):
        origIntRepr = self._intRepr()
        transposedIntRepr = origIntRepr + interval
        return Note._fromIntRepr(transposedIntRepr, self.duration, self.dot)
    
    def withDuration(self, duration):
        return Note(self.note, self.octave, duration, self.dot)
    
    def withOctave(self, octave):
        return Note(self.note, octave, self.duration, self.dot)
    
    def withDot(self):
        return Note(self.note, self.octave, self.duration, True)
    
    def withoutDot(self):
        return Note(self.note, self.octave, self.duration, False)
    
    def _intRepr(self):
        return self.octave * len(NotePitch) + self.note.value
    
    def __str__(self):
        return f"{self.note}({self.octave}')[{self.duration}{'.' if self.dot else ''}]"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def _fromIntRepr(intRepr, duration = 4, dot = False):
        note = NotePitch(intRepr % len(NotePitch))        
        octave = int(intRepr / len(NotePitch))
        return Note(note, octave, duration, dot)
        
    
    @staticmethod
    def checkInterval(a, b):
        return b._intRepr() - a._intRepr()
    
    @staticmethod
    def range(a, b):        
        return [Note._fromIntRepr(x) for x in range(a._intRepr(), b._intRepr()+1)]        
    
def intervalToString(interval):
    octaveInterval = int(abs(interval) / len(NotePitch))
    pitchInterval = abs(interval) % len(NotePitch)
    pitchIntervalName = {
        0: "1",
        1: "2m",
        2: "2M",
        3: "3m",
        4: "3M",
        5: "4",
        6: "5d/4A",
        7: "5",
        8: "6m",
        9: "6M",
        10: "7m",
        11: "7M"        
    }
    return (str(pitchIntervalName[pitchInterval]) + (f"(+{octaveInterval}')" if octaveInterval > 0 else ""))