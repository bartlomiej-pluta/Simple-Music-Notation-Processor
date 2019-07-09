from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import signature
from smnp.module.mic.lib.detector.noise import NoiseDetector
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofTypes

_signature1 = signature()
def _function1(env):
    nd = NoiseDetector()
    nd.waitForComplete()


_signature2 = signature(ofTypes(Type.INTEGER), ofTypes(Type.INTEGER))
def _function2(env, noiseTreshold, silenceTreshold):
    nd = NoiseDetector(noiseTreshold.value, silenceTreshold.value)
    nd.waitForComplete()


function = CombinedFunction(
    'wait',
    Function(_signature1, _function1),
    Function(_signature2, _function2)
)

