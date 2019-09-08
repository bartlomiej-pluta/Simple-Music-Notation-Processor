from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.module.synth.lib.wave import plot
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf

_signature = signature(listOf(Type.FLOAT))
def _function(env, wave):
    rawWave = [ m.value for m in wave.value ]
    plot(rawWave)


function = Function(_signature, _function, 'plot')
