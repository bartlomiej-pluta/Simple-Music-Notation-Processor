import sys
import time


def display(args, env):
    print("".join([arg.stringify() for arg in args]))


def objectType(args, env):
    if len(args) == 1:
        return args[0].stringify()
    else:
        pass # not valid signature


def exit(args, env):
    if len(args) == 1 and isinstance(args[0], int):
        sys.exit(args[0])
    else:
        pass # not valid signature


def sleep(args, env):
    if len(args) == 1 and isinstance(args[0], int):
        time.sleep(args[0])
    else:
        pass # not valid signature


def read(args, env):
    if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
        print(args[0], end="")
        value = input()
        if args[1] == "integer":
            try:
                return int(value)
            except ValueError as v:
                pass # not int
        elif args[1] == "string":
            return value
        # TODO: note - wydzielić parsowanie nut do osobnej funkcji w pakiecie smnp.note
        # elif args[1] == "note":
        #     chars, token = tokenizeNote(value, 0, 0)
        #     if chars == 0:
        #         return # not note
        #     return parseNote([token], None).value
        else:
            pass # invalid type
    elif len(args) == 1 and isinstance(args[0], str):
        print(args[0], end="")
        return input()
    elif len(args) == 0:
        return input()
    else:
        pass # not valid signature