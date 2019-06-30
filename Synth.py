import numpy as np
import sounddevice as sd
from Note import Note
import os
import sys
import time

FS = 44100 


def play(args, env):
    if len(args) > 0 and isinstance(args[0], list):
        playList(args[0], env)
        return    
    playList(args, env)    

def playList(notes, env):
    bpm = env.findVariable("bpm", int)
    if all(isinstance(x, Note) or isinstance(x, int) for x in notes):
        for x in notes:
            if isinstance(x, Note):
                playNote(x, bpm)
            if isinstance(x, int):
                doPause(x, bpm)     

def playNote(note, bpm):
    frequency = note.toFrequency()
    duration = 60 * 4 / note.duration / bpm
    sine(frequency, duration)       
    
def sine(frequency, duration):
    samples = (np.sin(2*np.pi*np.arange(FS*duration)*frequency/FS)).astype(np.float32)
    sd.play(samples, FS)    
    time.sleep(duration)
    
def doPause(value, bpm):
    time.sleep(60 * 4 / value / bpm)
    
def pause(args, env):
    bpm = findVariable("bpm", env)
    value = args[0]
    doPause(value, bpm)
