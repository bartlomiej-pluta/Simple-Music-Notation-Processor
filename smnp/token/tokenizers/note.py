import re

from smnp.note.model import Note
from smnp.token.model import Token
from smnp.token.type import TokenType


def noteTokenizer(input, current, line):
    consumedChars = 0
    notePitch = None
    octave = None
    duration = None
    dot = False
    rawValue = ''
    if input[current] == '@':
        rawValue += input[current+consumedChars]
        consumedChars += 1  # TODO: Check if next item does even exist
        if input[current+consumedChars] in ('C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'A', 'a', 'H', 'h', 'B', 'b'):
            rawValue += input[current + consumedChars]
            notePitch = input[current+consumedChars]
            consumedChars += 1
            
            if current+consumedChars < len(input) and input[current+consumedChars] in ('b', '#'):
                rawValue += input[current + consumedChars]
                notePitch += input[current+consumedChars]
                consumedChars += 1
                
            if current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):
                rawValue += input[current + consumedChars]
                octave = input[current+consumedChars]
                consumedChars += 1
                
            if current+consumedChars < len(input) and input[current+consumedChars] == ':':
                rawValue += input[current + consumedChars]
                duration = ''
                consumedChars += 1
                while current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):
                    rawValue += input[current + consumedChars]
                    duration += input[current+consumedChars]        
                    consumedChars += 1
                if len(duration) == 0:
                    return (0, None)
                dot = (current+consumedChars) < len(input) and input[current+consumedChars] == 'd'
                if dot:
                    rawValue += input[current + consumedChars]
                    consumedChars += 1

            octave = int(octave) if octave is not None else None
            duration = int(duration) if duration is not None else None
            value = Note(notePitch, octave, duration, dot)

            return (consumedChars, Token(TokenType.NOTE, value, (line, current), rawValue))
    return (0, None)
