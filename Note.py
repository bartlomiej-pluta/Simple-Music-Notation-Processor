from enum import Enum
from Error import ParseError

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
    def __init__(self, note, octave, duration):        
        if type(note) == str:            
            self.note = NotePitch.toPitch(note)
        else:
            self.note = note
        self.octave = octave
        self.duration = duration        
    
    @staticmethod
    def range(a, b):        
        return [Note(note, 1, 1) for note in NotePitch.range(a.note, b.note)]
