import time

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

from smnp.type.model import Type

FS = 44100


def pause(value, bpm):
    time.sleep(60 * 4 / value / bpm)


def plot(wave):
    X = np.arange(len(wave))
    plt.plot(X, wave)
    plt.show()


def play(wave):
    sd.play(wave)
    time.sleep(len(wave) / FS)


def compilePolyphony(notes, config):
    compiledLines = [1 / len(notes) * compileNotes(line, config) for line in notes]
    return sum(adjustSize(compiledLines))


def adjustSize(compiledLines):
    maxSize = max(len(line) for line in compiledLines)

    return [np.concatenate([line, np.zeros(maxSize - len(line))]) for line in compiledLines]


def compileNotes(notes, config):
    dispatcher = {
        Type.NOTE: lambda note, overtones: sineForNote(note.value, config),
        Type.INTEGER: lambda note, overtones: silenceForPause(note.value, config)
    }

    return np.concatenate([dispatcher[note.type](note, config) for note in notes])


def sineForNote(note, config):
    frequency = note.toFrequency()
    duration = 60 * 4 / note.duration / config.bpm
    duration *= 1.5 if note.dot else 1
    return sound(frequency, duration, config)


def sound(frequency, duration, config):
    return attack(decay(sum(overtone * sine((i+1) * frequency, duration) for i, overtone in enumerate(config.overtones) if overtone > 0), config), config)


def decay(wave, config):
    magnitude = np.exp(-config.decay/len(wave) * np.arange(len(wave)))

    return magnitude * wave


def attack(wave, config):
    magnitude = -np.exp(-config.attack / len(wave) * np.arange(len(wave)))+1 \
    if config.attack > 0 \
    else np.ones(len(wave))

    return magnitude * wave


def sine(frequency, duration):
    return (np.sin(2 * np.pi * np.arange(FS * duration) * frequency / FS)).astype(np.float32)


def silenceForPause(value, config):
    duration = 60 * 4 / value / config.bpm
    return np.zeros(int(FS * duration))
