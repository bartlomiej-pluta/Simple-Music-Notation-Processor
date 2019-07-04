import smnp.environment.function.list as l
from smnp.environment.environment import Environment
from smnp.environment.function import synth, base, interval, note, transposer, rand, mic
from smnp.environment.function.model import Function, ONLY_FUNCTION
from smnp.note.model import Note


def createEnvironment():
    functions = {
        'exit': Function(base.exit, ONLY_FUNCTION),
        'print': Function(base.display, ONLY_FUNCTION),
        'read': Function(base.read, ONLY_FUNCTION),
        'type': Function(base.objectType, ONLY_FUNCTION),
        'sleep': Function(base.sleep, ONLY_FUNCTION),
        'synth': Function(synth.synth, ONLY_FUNCTION),
        'pause': Function(synth.pause, ONLY_FUNCTION),
        'changeDuration': Function(note.changeDuration, ONLY_FUNCTION),
        'changeOctave': Function(note.changeOctave, ONLY_FUNCTION),
        'semitones': Function(interval.semitones, ONLY_FUNCTION),
        'interval': Function(interval.interval, ONLY_FUNCTION),
        'transpose': Function(transposer.transpose, ONLY_FUNCTION),
        'transposeTo': Function(transposer.transposeTo, ONLY_FUNCTION),
        'random': Function(rand.random, ONLY_FUNCTION),
        # 'sample': sample,
        'wait': Function(mic.wait, ONLY_FUNCTION),
        'tuplet': Function(note.tuplet, ONLY_FUNCTION),
        'combine': Function(l.combine, ONLY_FUNCTION),
        'flat': Function(l.flat, ONLY_FUNCTION),
        'debug': Function(lambda args, env: print(args), ONLY_FUNCTION),

    }

    methods = {
        str: {},
        list: {},
        float: {},
        Note: {
            'synth': synth.synth
        },
        type(None): {},
    }

    variables = {
        "bpm": 120
    }

    return Environment([ variables ], functions, methods)
 
