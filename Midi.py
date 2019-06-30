from Note import *
import Audio
import os
import sys
import time

def parseNotes(notes):
    map = { NotePitch.C: 'c', NotePitch.CIS: 'c#', NotePitch.D: 'd', NotePitch.DIS: 'd#',
           NotePitch.E: 'e', NotePitch.F: 'f', NotePitch.FIS: 'f#', NotePitch.G: 'g',
           NotePitch.GIS: 'g#', NotePitch.A: 'a', NotePitch.AIS: 'a#', NotePitch.H: 'b' }
    parsed = [(f"{map[note.note]}{note.octave}", note.duration) for note in notes]
    print(parsed)
  
def play(args, env):
    if len(args) > 0 and isinstance(args[0], list):
        playList(args[0], env)
        return    
    playList(args, env)        

def playList(notes, env):
    bpm = findVariable("bpm", env)
    if all(isinstance(x, Note) or isinstance(x, int) for x in notes):
        for x in notes:
            if isinstance(x, Note):
                Audio.playNote(x, bpm)
            if isinstance(x, int):
                doPause(x, bpm)
    #sys.stdout = open(os.devnull, 'w')
    #sys.stderr = open(os.devnull, 'w')
    #sys.stdout = sys.__stdout__
    #sys.stderr = sys.__stderr__    
    
def findVariable(name, environment):
    for scope in reversed(environment.scopes):
        if name in scope:
            return scope[name]

def pause(args, env):
    bpm = findVariable("bpm", env)
    value = args[0]
    doPause(value, bpm)
    
def doPause(value, bpm):
    time.sleep(60 * 4 / value / bpm)
