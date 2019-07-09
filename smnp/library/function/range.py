from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import signature, ofType
from smnp.note.model import Note
from smnp.type.model import Type


_signature1 = signature(ofType(Type.INTEGER))
def _function1(env, upper):
    return Type.list(list(range(upper.value + 1)))


_signature2 = signature(ofType(Type.INTEGER), ofType(Type.INTEGER))
def _function2(env, lower, upper):
    return Type.list(list(range(lower.value, upper.value + 1)))


_signature3 = signature(ofType(Type.INTEGER), ofType(Type.INTEGER), ofType(Type.INTEGER))
def _function3(env, lower, upper, step):
    return Type.list(list(range(lower.value, upper.value + 1, step.value)))


_signature4 = signature(ofType(Type.NOTE), ofType(Type.NOTE))
def _function4(env, lower, upper):
    return Type.list([Type.note(n) for n in Note.range(lower.value, upper.value)])


# TODO
# signature5 = range(note lower, note upper, integer step) OR step = "diatonic" | "chromatic" | "augmented" | "diminish"

function = CombinedFunction(
    'range',
    Function(_signature1, _function1),
    Function(_signature2, _function2),
    Function(_signature3, _function3),
    Function(_signature4, _function4),
)
