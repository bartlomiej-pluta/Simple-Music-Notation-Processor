from smnp.library.model import CombinedFunction, Function
from smnp.library.signature import signature, listOf, ofTypes, varargSignature
from smnp.type.model import Type
from smnp.type.value import Value


def _tuplet1(env, n, m, vararg):
    t = [Value(Type.NOTE, arg.value.withDuration(arg.value.duration * n.value / m.value)) for arg in vararg]
    return Value(Type.LIST, t).decompose()


_sign1 = varargSignature(ofTypes(Type.NOTE), ofTypes(Type.INTEGER), ofTypes(Type.INTEGER))



def _tuplet2(env, n, m, notes):
    return _tuplet1(env, n, m, notes.value)


_sign2 = signature(ofTypes(Type.INTEGER), ofTypes(Type.INTEGER), listOf(Type.NOTE))


tuplet = CombinedFunction(
    'tuplet',
    Function(_sign1, _tuplet1),
    Function(_sign2, _tuplet2)
)

# def tupletList(n, m, list):
#     return [note.withDuration(note.duration * n / m) for note in list]
#
#
# def tuplet(args, env):
#     if len(args) > 2 and type(args[0]) == int and type(args[1]) == int and all(type(x) == Note for x in args[2:]):
#         n = args[0] # how many notes
#         m = args[1] # instead of number of notes (3-tuplet: 3 instead 2; 5-tuplet: 5 instead 4 etc.)
#         return returnElementOrList(tupletList(n, m, args[2:]))
#     elif len(args) == 3 and type(args[0]) == int and type(args[1]) == int and type(args[2]) == list and all(type(x) == Note for x in args[2]):
#         n = args[0]
#         m = args[1]
#         l = args[2]
#         return returnElementOrList(tupletList(n, m, l))
#     else:
#         pass # not valid signature