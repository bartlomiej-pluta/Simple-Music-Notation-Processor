from smnp.environment.function.interval import semitonesList
from smnp.environment.function.tools import returnElementOrList
from smnp.note.model import Note


def transposeTo(args, env):
    if len(args) > 1 and isinstance(args[0], Note) and all(isinstance(x, list) for i, x in enumerate(args) if i != 0):
        target = args[0]
        result = []
        for i, notes in enumerate(args):
            if i == 0:
                continue
            if len(notes) > 0:
                first = notes[0]
                semitones = semitonesList([first, target])[0]
                result.append([note.transpose(semitones) for note in notes if isinstance(note, Note)])
            else:
                result.append([])
        return returnElementOrList(result)
    else:
        pass  # not valid signature


def transpose(args, env):
    if len(args) > 1 and isinstance(args[0], int) and all(
            isinstance(arg, list) for i, arg in enumerate(args) if i != 0):
        value = args[0]
        transposed = []
        for i, arg in enumerate(args):
            if i == 0:
                continue
            if not isinstance(arg, list):
                return  # is not list
            transposed.append([note.transpose(value) for note in arg if isinstance(note, Note)])
        return returnElementOrList(transposed)
    if len(args) > 1 and all(isinstance(arg, Note) for i, arg in enumerate(args) if i != 0):
        value = args[0]
        transposed = [note.transpose(value) for i, note in enumerate(args) if i != 0]
        return returnElementOrList(transposed)
    else:
        return  # not valid signature
