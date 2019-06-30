import pysine
from Note import Note, NotePitch
import time

BREAK = 0

def playNote(note, bpm):
    frequency = note.toFrequency()
    duration = 60 * 4 / note.duration / bpm
    pysine.sine(frequency, duration)    
    #TODO: duration powinno byc w prawdziwych nutach: 4 = cwierc, 2 = pol etc.

    
