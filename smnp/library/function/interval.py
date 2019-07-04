from smnp.library.tools import returnElementOrList
from smnp.note.interval import intervalToString
from smnp.note.model import Note


def interval(args, env):
    if len(args) > 0 and isinstance(args[0], list):
        return intervalList(args[0])
    return intervalList(args)


def intervalList(list):
    r = [intervalToString(x) for x in semitonesList(list)]
    return returnElementOrList(r)

def semitonesList(list):
    for x in list:
        if not isinstance(x, Note) and not isinstance(x, int):
            pass # invalid arguments
    withoutPauses = tuple(filter(lambda x: isinstance(x, Note), list))
    r = [Note.checkInterval(withoutPauses[i-1], withoutPauses[i]) for i, _ in enumerate(withoutPauses) if i != 0]
    return r

def semitones(args, env):
    if len(args) > 0 and isinstance(args[0], list):
        return returnElementOrList(semitonesList(args[0]))
    return returnElementOrList(semitonesList(args))