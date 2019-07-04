import time

from smnp.library.model import Function
from smnp.library.signature import ofTypes, signature
from smnp.type.model import Type


def _sleep(env, value):
    time.sleep(value.value)

_sign = signature(ofTypes(Type.INTEGER))

sleep = Function(_sign, _sleep, 'sleep')