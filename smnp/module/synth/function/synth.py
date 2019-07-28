from smnp.error.runtime import RuntimeException
from smnp.function.model import Function, CombinedFunction
from smnp.function.signature import varargSignature
from smnp.module.synth.lib.wave import play

from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf
from smnp.type.signature.matcher.type import ofTypes, ofType


DEFAULT_BPM = 120
DEFAULT_OVERTONES = [0.4, 0.3, 0.1, 0.1, 0.1]


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
        if overtones.type != Type.LIST or not all(overtone.type == Type.FLOAT for overtone in overtones.value):
            raise RuntimeException("The 'overtones' property must be list of floats", None)

        if len(rawOvertones) < 1:
            raise RuntimeException("The 'overtones' property must contain one overtone at least", None)

        if any(overtone < 0 for overtone in rawOvertones):
            raise RuntimeException("The 'overtones' property mustn't contain negative values", None)

        if sum(rawOvertones) > 1.0:
            raise RuntimeException("The 'overtones' property must contain overtones which sum is not greater than 1.0", None)

        return rawOvertones

    return DEFAULT_OVERTONES


_signature1 = varargSignature(listOf(Type.NOTE, Type.INTEGER), ofType(Type.MAP))
def _function1(env, config, notes):
    rawNotes = [note.value for note in notes]
    bpm = getBpm(config)
    overtones = getOvertones(config)

    play(rawNotes, bpm, overtones)


_signature2 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER), ofType(Type.MAP))
def _function2(env, config, notes):
    bpm = getBpm(config)
    overtones = getOvertones(config)
    play([ notes ], bpm, overtones)


function = CombinedFunction(
    'synth',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)