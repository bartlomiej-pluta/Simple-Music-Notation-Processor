from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.module.synth.lib.player import play
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = signature(ofType(Type.NOTE))
def _function(env, note):
    bpm = env.findVariable('bpm')
    play(note.value, bpm.value)


function = Function(_signature, _function, 'synthNote')