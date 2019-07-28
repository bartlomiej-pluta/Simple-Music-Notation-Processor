from smnp.function.model import Function, CombinedFunction
from smnp.function.signature import varargSignature
from smnp.module.synth.lib.wave import play

from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf
from smnp.type.signature.matcher.type import ofTypes

_signature1 = varargSignature(listOf(Type.NOTE, Type.INTEGER))
def _function1(env, notes):
    rawNotes = [note.value for note in notes]
    play(rawNotes, env.findVariable("bpm").value, env.findVariable("overtones").value)


_signature2 = varargSignature(ofTypes(Type.NOTE, Type.INTEGER))
def _function2(env, notes):
    play([ notes ], env.findVariable("bpm").value, env.findVariable("overtones").value)


function = CombinedFunction(
    'synth',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)