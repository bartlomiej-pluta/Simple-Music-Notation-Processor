from smnp.error.runtime import RuntimeException
from smnp.function.model import Function, CombinedFunction
from smnp.function.signature import varargSignature
from smnp.module.synth.lib.wave import compilePolyphony

from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf
from smnp.type.signature.matcher.type import ofTypes, ofType


DEFAULT_BPM = 120
DEFAULT_OVERTONES = [0.4, 0.3, 0.1, 0.1, 0.1]
DEFAULT_DECAY = 4
DEFAULT_ATTACK = 100


def getBpm(config):
    key = Type.string("bpm")
    if key in config.value:
        bpm = config.value[key]
        if bpm.type != Type.INTEGER or bpm.value <= 0:
            raise RuntimeException("The 'bpm' property must be positive integer", None)

        return bpm.value

    return DEFAULT_BPM


def getOvertones(config):
    key = Type.string("overtones")
    if key in config.value:
        overtones = config.value[key]
        rawOvertones = [overtone.value for overtone in overtones.value]
        if overtones.type != Type.LIST or not all(overtone.type in [Type.FLOAT, Type.INTEGER] for overtone in overtones.value):
            raise RuntimeException("The 'overtones' property must be list of floats", None)

        if len(rawOvertones) < 1:
            raise RuntimeException("The 'overtones' property must contain one overtone at least", None)

        if any(overtone < 0 for overtone in rawOvertones):
            raise RuntimeException("The 'overtones' property mustn't contain negative values", None)

        if sum(rawOvertones) > 1.0:
            raise RuntimeException("The 'overtones' property must contain overtones which sum is not greater than 1.0", None)

        return rawOvertones

    return DEFAULT_OVERTONES


def getDecay(config):
    key = Type.string("decay")
    if key in config.value:
        decay = config.value[key]
        if not decay.type in [Type.INTEGER, Type.FLOAT] or decay.value < 0:
            raise RuntimeException("The 'decay' property must be non-negative integer or float", None)

        return decay.value

    return DEFAULT_DECAY


def getAttack(config):
    key = Type.string("attack")
    if key in config.value:
        attack = config.value[key]
        if not attack.type in [Type.INTEGER, Type.FLOAT] or attack.value < 0:
            raise RuntimeException("The 'attack' property must be non-negative integer or float", None)

        return attack.value

    return DEFAULT_ATTACK


class Config:
    def __init__(self, bpm, overtones, decay, attack):
        self.bpm = bpm
        self.overtones = overtones
        self.decay = decay
        self.attack = attack

    @staticmethod
    def default():
        return Config(DEFAULT_BPM, DEFAULT_OVERTONES, DEFAULT_DECAY, DEFAULT_ATTACK)


_signature1 = varargSignature(listOf(Type.NOTE, Type.INTEGER))
def _function1(env, notes):
    return Type.list([Type.float(float(m)) for m in __function1(notes)])


def __function1(notes):
    return compilePolyphony([note.value for note in notes], Config.default())


_signature2 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))
def _function2(env, notes):
    return Type.list([Type.float(float(m)) for m in __function2(notes)])


def __function2(notes):
    return compilePolyphony([ notes ], Config.default())


_signature3 = varargSignature(listOf(Type.NOTE, Type.INTEGER), ofType(Type.MAP))
def _function3(env, config, notes):
    return Type.list([ Type.float(float(m)) for m in __function3(config, notes) ])


def __function3(config, notes):
    rawNotes = [note.value for note in notes]

    bpm = getBpm(config)
    overtones = getOvertones(config)
    decay = getDecay(config)
    attack = getAttack(config)

    return compilePolyphony(rawNotes, Config(bpm, overtones, decay, attack))


_signature4 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER), ofType(Type.MAP))
def _function4(env, config, notes):
    return Type.list([ Type.float(float(m)) for m in __function4(config, notes) ])


def __function4(config, notes):
    bpm = getBpm(config)
    overtones = getOvertones(config)
    decay = getDecay(config)
    attack = getAttack(config)

    return compilePolyphony([ notes ], Config(bpm, overtones, decay, attack))


function = CombinedFunction(
    'wave',
    Function(_signature1, _function1),
    Function(_signature2, _function2),
    Function(_signature3, _function3),
    Function(_signature4, _function4),
)