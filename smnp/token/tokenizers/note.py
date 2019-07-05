import re

from smnp.note.model import Note
from smnp.token.model import Token
from smnp.token.type import TokenType


def tokenizeNote(input, current, line):
    consumedChars = 0
    notePitch = None
    octave = None
    duration = None
    dot = False
    if input[current] == '@':
        consumedChars += 1
        if input[current+consumedChars] in ('C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'A', 'a', 'H', 'h', 'B', 'b'):
            notePitch = input[current+consumedChars]
            consumedChars += 1
            
            if current+consumedChars < len(input) and input[current+consumedChars] in ('b', '#'):                        
                notePitch += input[current+consumedChars]
                consumedChars += 1
                
            if current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):            
                octave = input[current+consumedChars]
                consumedChars += 1
                
            if current+consumedChars < len(input) and input[current+consumedChars] == '.':
                duration = ''
                consumedChars += 1
                while current+consumedChars < len(input) and re.match(r'\d', input[current+consumedChars]):
                    duration += input[current+consumedChars]        
                    consumedChars += 1
                if len(duration) == 0:
                    return (0, None)
                dot = (current+consumedChars) < len(input) and input[current+consumedChars] == 'd'
                consumedChars += 1

            octave = int(octave) if octave is not None else None
            duration = int(duration) if duration is not None else None
            value = Note(notePitch, octave, duration, dot)

            return (consumedChars, Token(TokenType.NOTE, value, (line, current)))
    return (0, None)
