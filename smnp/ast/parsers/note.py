import re

from smnp.ast.node.note import NoteLiteralNode
from smnp.note.model import Note
from smnp.token.type import TokenType


# note -> NOTE
def parseNote(input, parent):
    if input.current().type == TokenType.NOTE:
        token = input.current()
        value = token.value
        consumedChars = 1
        notePitch = value[consumedChars]
        consumedChars += 1
        octave = 4
        duration = 4
        dot = False
        if consumedChars < len(value) and value[consumedChars] in ('b', '#'):
            notePitch += value[consumedChars]
            consumedChars += 1
        if consumedChars < len(value) and re.match(r'\d', value[consumedChars]):
            octave = int(value[consumedChars])
            consumedChars += 1
        if consumedChars < len(value) and value[consumedChars] == '.':
            consumedChars += 1
            durationString = ''
            while consumedChars < len(value) and re.match(r'\d', value[consumedChars]):
                durationString += value[consumedChars]
                consumedChars += 1
                duration = int(durationString)
            if consumedChars < len(value) and value[consumedChars] == 'd':
                dot = True
                consumedChars += 1

        input.ahead()
        return NoteLiteralNode(Note(notePitch, octave, duration, dot), parent, token.pos)
    return None