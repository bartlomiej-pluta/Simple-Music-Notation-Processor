import numpy as np

from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.list import listOf

_signature = signature(listOf(Type.FLOAT))
def _function(env, signal):
    raw = [ x.value for x in signal.value ]
    N = len(raw)
    fft = np.fft.fft(raw)/N
    fft = fft[range(int(N/2))]
    return Type.list([ Type.float(float(abs(x))) for x in fft ])


function = Function(_signature, _function, 'fft')