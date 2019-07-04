from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.synth import player
from smnp.type.model import Type


def _pause(env, value):
    bpm = env.findVariable('bpm')
    player.pause(value.value, bpm)


_sign = signature(ofTypes(Type.INTEGER))


pause = Function(_sign, _pause, 'pause')