from enum import Enum

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
    
    @staticmethod
    def toPitch(string):
        map = { 'c': NotePitch.C, 'c#': NotePitch.CIS, 'db': NotePitch.CIS, 'd': NotePitch.D,
               'd#': NotePitch.DIS, 'eb': NotePitch.DIS, 'e': NotePitch.E, 'fb': NotePitch.E, 'e#': NotePitch.F,
               'f': NotePitch.F, 'f#': NotePitch.FIS, 'gb': NotePitch.FIS, 'g': NotePitch.G, 'g#': NotePitch.GIS,
               'ab': NotePitch.GIS, 'a': NotePitch.A, 'a#': NotePitch.AIS, 'b': NotePitch.AIS, 'h': NotePitch.H
               }
        return map[string.lower()]

class Note:
    def __init__(self, note, octave, duration):        
        if type(note) == str:            
            self.note = NotePitch.toPitch(note)
        else:
            self.note = note
        self.octave = octave
        self.duration = duration
        
    def __str__(self):
        return f"{self.note}[{self.octave}, {self.duration}]"
