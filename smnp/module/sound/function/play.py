from smnp.library.model import Function
from smnp.library.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = signature(ofType(Type.SOUND))
def _function(env, sound):
    sound.value.play()


function = Function(_signature, _function, 'play')
