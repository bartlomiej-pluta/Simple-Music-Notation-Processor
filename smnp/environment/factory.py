from smnp.environment.environment import Environment
from smnp.library.function import display, sleep, semitones, interval, combine, flat, wait, rand, tuplet, synth, pause, \
    transpose, type, exit, duration, octave, debug
from smnp.type.model import Type
from smnp.type.value import Value


def createEnvironment():
    functions = [
        display.function,
        type.function,
        exit.function,
        sleep.function,
        semitones.function,
        interval.function,
        combine.function,
        flat.function,
        wait.function,
        rand.function,
        tuplet.function,
        synth.function,
        pause.function,
        transpose.function,
        debug.function
    ]

    methods = [
        duration.function,
        octave.function,
    ]

    variables = {
        "bpm": Value(Type.INTEGER, 120)
    }

    return Environment([ variables ], functions, methods)
 
