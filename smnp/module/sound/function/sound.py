from smnp.audio.sound import Sound
from smnp.function.model import Function
from smnp.function.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature = signature(ofType(Type.STRING))
def _function(env, file):
    return Type.sound(Sound(file.value))


function = Function(_signature, _function, 'Sound')