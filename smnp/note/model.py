from smnp.note.pitch import NotePitch

class Note:
    def __init__(self, note, octave, duration, dot = False):
        if octave is None:
            octave = 4

        if duration is None:
            duration = 4

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
    def checkInterval(a, b):
        return b._intRepr() - a._intRepr()
    
    @staticmethod
    def range(a, b):        
        return [Note._fromIntRepr(x) for x in range(a._intRepr(), b._intRepr()+1)] 
    
    @staticmethod
    def _fromIntRepr(intRepr, duration = 4, dot = False):
        note = NotePitch(intRepr % len(NotePitch))        
        octave = int(intRepr / len(NotePitch))
        return Note(note, octave, duration, dot)
