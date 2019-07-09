from smnp.library.model import Function
from smnp.library.signature import signature, ofType
from smnp.type.model import Type


_signature = signature(ofType(Type.SOUND))
def _function(env, sound):
    sound.value.play()


function = Function(_signature, _function, 'play')
