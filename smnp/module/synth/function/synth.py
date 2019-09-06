from smnp.function.model import Function, CombinedFunction
from smnp.function.signature import varargSignature
from smnp.module.synth.function import compile
from smnp.module.synth.lib.wave import play
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf
from smnp.type.signature.matcher.type import ofTypes, ofType

_signature1 = varargSignature(listOf(Type.NOTE, Type.INTEGER))
def _function1(env, notes):
    wave = compile.__function1(notes)
    play(wave)


_signature2 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))
def _function2(env, notes):
    wave = compile.__function2(notes)
    play(wave)


_signature3 = varargSignature(listOf(Type.NOTE, Type.INTEGER), ofType(Type.MAP))
def _function3(env, config, notes):
    wave = compile.__function3(config, notes)
    play(wave)


_signature4 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER), ofType(Type.MAP))
def _function4(env, config, notes):
    wave = compile.__function4(config, notes)
    play(wave)


_signature5 = varargSignature(listOf(Type.FLOAT))
def _function5(env, waves):
    for wave in waves:
        rawWave = [m.value for m in wave.value]
        play(rawWave)


function = CombinedFunction(
    'synth',
    Function(_signature1, _function1),
    Function(_signature2, _function2),
    Function(_signature3, _function3),
    Function(_signature4, _function4),
    Function(_signature5, _function5)
)