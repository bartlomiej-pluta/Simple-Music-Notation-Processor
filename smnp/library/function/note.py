from smnp.library.tools import returnElementOrList


def changeDuration(args, env):
    if len(args) == 2 and isinstance(args[0], Note) and isinstance(args[1], int):
        return args[0].withDuration(args[1])
    return # invalid signature


def changeOctave(args, env):
    if len(args) == 2 and isinstance(args[0], Note) and isinstance(args[1], int):
        return args[0].withOctave(args[1])
    return # invalid signature


def tupletList(n, m, list):
    return [note.withDuration(note.duration * n / m) for note in list]


def tuplet(args, env):
    if len(args) > 2 and type(args[0]) == int and type(args[1]) == int and all(type(x) == Note for x in args[2:]):
        n = args[0] # how many notes
        m = args[1] # instead of number of notes (3-tuplet: 3 instead 2; 5-tuplet: 5 instead 4 etc.)
        return returnElementOrList(tupletList(n, m, args[2:]))
    elif len(args) == 3 and type(args[0]) == int and type(args[1]) == int and type(args[2]) == list and all(type(x) == Note for x in args[2]):
        n = args[0]
        m = args[1]
        l = args[2]
        return returnElementOrList(tupletList(n, m, l))
    else:
        pass # not valid signature