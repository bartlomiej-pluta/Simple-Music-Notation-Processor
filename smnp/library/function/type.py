from smnp.library.model import Function
from smnp.library.signature import signature, allTypes


def _objectType(env, obj):
    return obj.type.name

_sign = signature(allTypes())

objectType = Function(_sign, _objectType, 'type')