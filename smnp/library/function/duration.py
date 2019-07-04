from smnp.library.model import Function
from smnp.library.signature import signature, ofTypes
from smnp.type.model import Type
from smnp.type.value import Value


_signature = signature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER))
def _function(env, note, duration):
    return Value(Type.NOTE, note.value.withDuration(duration.value))


function = Function(_signature, _function, 'withDuration')