from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.module.synth.lib import player
from smnp.type.model import Type


_signature = signature(ofTypes(Type.INTEGER))
def _function(env, value):
    bpm = env.findVariable('bpm')
    player.pause(value.value, bpm.value)


function = Function(_signature, _function, 'pause')