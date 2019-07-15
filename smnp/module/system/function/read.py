from smnp.error.runtime import RuntimeException
from smnp.function.model import CombinedFunction, Function
from smnp.function.signature import signature
from smnp.token.tokenizers.bool import boolTokenizer
from smnp.token.tokenizers.note import noteTokenizer
from smnp.type.model import Type
from smnp.type.signature.matcher.type import ofType

_signature1 = signature()
def _function1(env):
    value = input()
    return Type.string(value)


_signature2 = signature(ofType(Type.STRING))
def _function2(env, prompt):
    print(prompt.value, end="")
    value = input()
    return Type.string(value)


_signature3 = signature(ofType(Type.TYPE))
def _function3(env, type):
    value = input()
    return getValueAccordingToType(value, type)


def getValueAccordingToType(value, type):
    try:
        if type.value == Type.STRING:
            return Type.string(value)

        if type.value == Type.INTEGER:
            return Type.integer(int(value))

        if type.value == Type.BOOL:
            consumedChars, token = boolTokenizer(value, 0, 0)
            if consumedChars > 0:
                return Type.bool(token.value)

            return ValueError()

        if type.value == Type.NOTE:
            consumedChars, token = noteTokenizer(value, 0, 0)
            if consumedChars > 0:
                return Type.note(token.value)

            raise ValueError()

        raise RuntimeException(f"Type {type.value.name.lower()} is not suuported", None)

    except ValueError:
        raise RuntimeException(f"Invalid value '{value}' for type {type.value.name.lower()}", None)


_signature4 = signature(ofType(Type.STRING), ofType(Type.TYPE))
def _function4(env, prompt, type):
    print(prompt.value, end="")
    value = input()
    return getValueAccordingToType(value, type)


function = CombinedFunction(
    'read',
    Function(_signature1, _function1),
    Function(_signature2, _function2),
    Function(_signature3, _function3),
    Function(_signature4, _function4)
)

# TODO read function
# def read(args, env):
#     if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
#         print(args[0], end="")
#         value = input()
#         if args[1] == "integer":
#             try:
#                 return int(value)
#             except ValueError as v:
#                 pass # not int
#         elif args[1] == "string":
#             return value
#         # TODO: note - wydzielić parsowanie nut do osobnej funkcji w pakiecie smnp.note
#         # elif args[1] == "note":
#         #     chars, token = tokenizeNote(value, 0, 0)
#         #     if chars == 0:
#         #         return # not note
#         #     return parseNote([token], None).value
#         else:
#             pass # invalid type
#     elif len(args) == 1 and isinstance(args[0], str):
#         print(args[0], end="")
#         return input()
#     elif len(args) == 0:
#         return input()
#     else:
#         pass # not valid signature