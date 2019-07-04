import time

from smnp.note.model import Note
from smnp.synth.wave import sine


def playNotes(notes, bpm):
    for note in notes:
        {
            Note: play,
            int: pause
        }[type(note)](note, bpm)


def play(note, bpm):
    frequency = note.toFrequency()
    duration = 60 * 4 / note.duration / bpm
    duration *= 1.5 if note.dot else 1
    sine(frequency, duration)


def pause(value, bpm):
    time.sleep(60 * 4 / value / bpm)

