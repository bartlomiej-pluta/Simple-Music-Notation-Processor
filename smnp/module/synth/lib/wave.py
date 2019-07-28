import time

import numpy as np
import sounddevice as sd

from smnp.type.model import Type

FS = 44100


def pause(value, bpm):
    time.sleep(60 * 4 / value / bpm)


def play(notes, bpm, overtones):
    compiled = compilePolyphony(notes, bpm, overtones)
    sd.play(compiled)
    time.sleep(len(compiled) / FS)


def compilePolyphony(notes, bpm, overtones):
    compiledLines = [1 / len(notes) * compileNotes(line, bpm, overtones) for line in notes]
    return sum(adjustSize(compiledLines))


def adjustSize(compiledLines):
    maxSize = max(len(line) for line in compiledLines)

    return [np.concatenate([line, np.zeros(maxSize - len(line))]) for line in compiledLines]


def compileNotes(notes, bpm, overtones):
    dispatcher = {
        Type.NOTE: lambda note, overtones: sineForNote(note.value, bpm, overtones),
        Type.INTEGER: lambda note, overtones: silenceForPause(note.value, bpm)
    }

    return np.concatenate([dispatcher[note.type](note, overtones) for note in notes])


def sineForNote(note, bpm, overtones):
    frequency = note.toFrequency()
    duration = 60 * 4 / note.duration / bpm
    duration *= 1.5 if note.dot else 1
    return sound(frequency, duration, overtones)


def sound(frequency, duration, overtones):
    return sum(a.value * sine((i+1) * frequency, duration) for i, a in enumerate(overtones))


def sine(frequency, duration):
    return (np.sin(2 * np.pi * np.arange(FS * duration) * frequency / FS)).astype(np.float32)


def silenceForPause(value, bpm):
    duration = 60 * 4 / value / bpm
    return np.zeros(int(FS * duration))
