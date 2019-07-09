from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import varargSignature, ofTypes, listOf
from smnp.module.synth.lib.player import playNotes
from smnp.type.model import Type


_signature1 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))
def _function1(env, vararg):
    notes = [arg.value for arg in vararg]
    bpm = env.findVariable('bpm')
    playNotes(notes, bpm.value)


_signature2 = varargSignature(listOf(Type.NOTE, Type.INTEGER))
def _function2(env, vararg):
    for arg in vararg:
        _function1(env, arg.value)


function = CombinedFunction(
    'synth',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)
