from smnp.environment.environment import Environment
from smnp.library.function.combine import combine
from smnp.library.function.display import display
from smnp.library.function.duration import withDuration
from smnp.library.function.exit import exit
from smnp.library.function.flat import flat
from smnp.library.function.interval import interval
from smnp.library.function.mic import wait
from smnp.library.function.octave import withOctave
from smnp.library.function.rand import random
from smnp.library.function.semitones import semitones
from smnp.library.function.sleep import sleep
from smnp.library.function.synth import synth
from smnp.library.function.tuplet import tuplet
from smnp.library.function.type import objectType


def createEnvironment():
    functions = [
        display,
        objectType,
        exit,
        sleep,
        semitones,
        interval,
        combine,
        flat,
        wait,
        random,
        tuplet,
        synth
    ]

    methods = [
        withDuration,
        withOctave
    ]
        # 'exit': Function(base.exit, ONLY_FUNCTION),
        # 'print': Function(base.display, ONLY_FUNCTION),
        # 'read': Function(base.read, ONLY_FUNCTION),
        # 'type': Function(base.objectType, ONLY_FUNCTION),
        # 'sleep': Function(base.sleep, ONLY_FUNCTION),
        # 'synth': Function(synth.synth, ONLY_FUNCTION),
        # 'pause': Function(synth.pause, ONLY_FUNCTION),
        # 'changeDuration': Function(note.changeDuration, ONLY_FUNCTION),
        # 'changeOctave': Function(note.changeOctave, ONLY_FUNCTION),
        # 'semitones': Function(interval.semitones, ONLY_FUNCTION),
        # 'interval': Function(interval.interval, ONLY_FUNCTION),
        # 'transpose': Function(transposer.transpose, ONLY_FUNCTION),
        # 'transposeTo': Function(transposer.transposeTo, ONLY_FUNCTION),
        # 'random': Function(rand.random, ONLY_FUNCTION),
        # # 'sample': sample,
        # 'wait': Function(mic.wait, ONLY_FUNCTION),
        # 'tuplet': Function(note.tuplet, ONLY_FUNCTION),
        # 'combine': Function(l.combine, ONLY_FUNCTION),
        # 'flat': Function(l.flat, ONLY_FUNCTION),
        # 'debug': Function(lambda args, env: print(args), ONLY_FUNCTION),


    # methods = {
    #     str: {},
    #     list: {},
    #     float: {},
    #     Note: {
    #         'synth': synth.synth
    #     },
    #     type(None): {},
    # }

    variables = {
        "bpm": 120
    }

    return Environment([ variables ], functions, methods)
 
