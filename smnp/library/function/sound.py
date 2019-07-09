from smnp.audio.sound import Sound
from smnp.library.model import Function
from smnp.library.signature import signature, ofType
from smnp.type.model import Type

_signature = signature(ofType(Type.STRING))
def _function(env, file):
    return Type.sound(Sound(file.value))

function = Function(_signature, _function, 'Sound')