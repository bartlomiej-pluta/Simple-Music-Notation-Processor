from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import signature, ofTypes
from smnp.mic.detector.noise import NoiseDetector
from smnp.type.model import Type


def _wait1(env):
    nd = NoiseDetector()
    nd.waitForComplete()


_sign1 = signature()


def _wait2(env, noiseTreshold, silenceTreshold):
    nd = NoiseDetector(noiseTreshold.value, silenceTreshold.value)
    nd.waitForComplete()


_sign2 = signature(ofTypes(Type.INTEGER), ofTypes(Type.INTEGER))


wait = CombinedFunction(
    'wait',
    Function(_sign1, _wait1),
    Function(_sign2, _wait2)
)

