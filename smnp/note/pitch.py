from enum import Enum

from smnp.error.syntax import SyntaxException


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
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()    
    
    #@staticmethod
    #def checkInterval(a, b):
        #return a.value - b.value
    
    @staticmethod
    def toPitch(string): #TODO: token zamiast stringa, żeby można było wziąć pos
        try:            
            return stringToPitch[string.lower()]
        except KeyError as e:
            raise SyntaxException(f"Note '{string}' does not exist") #TODO jakis inny exception

stringToPitch = {
    'c': NotePitch.C,
    'c#': NotePitch.CIS,
    'db': NotePitch.CIS,
    'd': NotePitch.D,
    'd#': NotePitch.DIS,
    'eb': NotePitch.DIS,
    'e': NotePitch.E,
    'fb': NotePitch.E,
    'e#': NotePitch.F,
    'f': NotePitch.F,
    'f#': NotePitch.FIS,
    'gb': NotePitch.FIS,
    'g': NotePitch.G,
    'g#': NotePitch.GIS,
    'ab': NotePitch.GIS,
    'a': NotePitch.A,
    'a#': NotePitch.AIS,
    'b': NotePitch.AIS,
    'h': NotePitch.H
}