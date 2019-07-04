from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import varargSignature, ofTypes, listOf
from smnp.synth.player import playNotes
from smnp.type.model import Type


def _synth1(env, vararg):
    notes = [arg.value for arg in vararg]
    bpm = env.findVariable('bpm')
    playNotes(notes, bpm)


_sign1 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))


def _synth2(env, vararg):
    for arg in vararg:
        _synth1(env, arg.value)


_sign2 = varargSignature(listOf(Type.NOTE, Type.INTEGER))


synth = CombinedFunction(
    'synth',
    Function(_sign1, _synth1),
    Function(_sign2, _synth2)
)
