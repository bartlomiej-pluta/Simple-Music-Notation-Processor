from smnp.environment.environment import Environment
from smnp.library.function import display, sleep, semitones, interval, combine, flat, wait, rand, tuplet, synth, pause, \
    transpose, type, exit, duration, octave, debug, get
from smnp.type.model import Type


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
        get.function
    ]

    variables = {
        "bpm": Type.integer(120)
    }

    return Environment([ variables ], functions, methods)
 
