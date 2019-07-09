from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.module.synth.lib import player
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature = signature(ofTypes(Type.INTEGER))
def _function(env, value):
    bpm = env.findVariable('bpm')
    player.pause(value.value, bpm.value)


function = Function(_signature, _function, 'pause')