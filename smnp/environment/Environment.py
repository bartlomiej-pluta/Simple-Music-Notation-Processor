import sys
from parser.Environment import objectString
from Note import *
import random
import Synth
import time
from Error import RuntimeException
from NoiseDetector import waitForSound
from Parser import parseNote
from Tokenizer import Token, TokenType, tokenizeNote
from functools import reduce

types = {
    int: 'integer',
    str: 'string',
    list: 'list',
    float: 'percent',
    Note: 'note', 
    type(None): 'void'
}

class Environment():
    def __init__(self, scopes, functions, methods):
        self.scopes = scopes
        self.functions = functions
        self.methods = methods
        self.customFunctions = {}
        self.callStack = []        
    
    def findVariable(self, name, type=None):
        for scope in reversed(self.scopes):
            if name in scope:
                value = scope[name]
                if type is not None:
                    if isinstance(value, type): 
                        return value         
                else:
                    return value
        raise RuntimeException(None, f"Variable '{name}' is not declared" + ("" if type is None else f" (expected type: {types[type]})"))
    
    def findVariableScope(self, name, type=None):
        for scope in reversed(self.scopes):
            if name in scope:                
                if type is not None:
                    if isinstance(scope[name], type): 
                        return scope         
                else:
                    return scope        
 
def doPrint(args, env):    
    print("".join([objectString(arg) for arg in args]))

def semitonesList(list):
    for x in list:
        if not isinstance(x, Note) and not isistance(x, int):
            pass # invalid arguments
    withoutPauses = tuple(filter(lambda x: isinstance(x, Note), list))    
    r = [Note.checkInterval(withoutPauses[i-1], withoutPauses[i]) for i, _ in enumerate(withoutPauses) if i != 0]
    return r

def returnElementOrList(list):
    return list[0] if len(list) == 1 else list

def semitones(args, env):
    if len(args) > 0 and isinstance(args[0], list):
        return returnElementOrList(semitonesList(args[0]))
    return returnElementOrList(semitonesList(args))

def intervalList(list):    
    r = [intervalToString(x) for x in semitonesList(list)]
    return returnElementOrList(r)

def interval(args, env):    
    if len(args) > 0 and isinstance(args[0], list):        
        return intervalList(args[0])
    return intervalList(args)

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
        pass # not valid signature
                
 
def transpose(args, env):    
    if len(args) > 1 and isinstance(args[0], int) and all(isinstance(arg, list) for i, arg in enumerate(args) if i != 0):
        value = args[0]
        transposed = []
        for i, arg in enumerate(args):            
            if i == 0:
                continue
            if not isinstance(arg, list):
                return # is not list            
            transposed.append([note.transpose(value) for note in arg if isinstance(note, Note)])
        return returnElementOrList(transposed)
    if len(args) > 1 and all(isinstance(arg, Note) for i, arg in enumerate(args) if i != 0):        
        value = args[0]
        transposed = [note.transpose(value) for i, note in enumerate(args) if i != 0]
        return returnElementOrList(transposed)
    else:
        return # not valid signature

def objectType(args, env):
    if len(args) == 1:
        return types[type(args[0])]
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

def rand(args, env):
    if not all(isinstance(x, list) and len(x) == 2 and isinstance(x[0], float) for x in args):
        return # not valid signature
    if sum([x[0] for x in args]) != 1.0:
        return # not sums to 100%
    choice = random.random()
    acc = 0
    for e in args:
        acc += e[0]
        if choice <= acc:
            return e[1]

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
        elif args[1] == "note":       
            chars, token = tokenizeNote(value, 0, 0)
            if chars == 0:                
                return # not note            
            return parseNote([token], None).value
        else:
            pass # invalid type
    elif len(args) == 1 and isinstance(args[0], str):
        print(args[0], end="")
        return input()
    elif len(args) == 0:
        return input()
    else:
        pass # not valid signature

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

def combine(args, env):
    if all(type(x) == list for x in args):
        return reduce((lambda x, y: x + y), args)

def flat(args, env):
    return _flat(args, [])

def _flat(input, output = []):
    for item in input:
        if type(item) == list:
            _flat(item, output)
        else:
            output.append(item)
    return output

def createEnvironment():
    functions = {
        'print': doPrint,
        'synth': Synth.play,
        'pause': Synth.pause,
        'type': objectType,
        'sample': sample,
        'semitones': semitones,
        'interval': interval,
        'transpose': transpose,   
        'transposeTo': transposeTo,
        'sleep': sleep,
        'random': rand,
        'changeDuration': changeDuration,
        'changeOctave': changeOctave,
        'wait': waitForSound,
        'read': read,
        'debug': lambda args, env: print(args),
        'tuplet': tuplet,
        'combine': combine,
        'flat': flat,
        'exit': exit
        
    }
    
    methods = {
        str: {},
        list: {},
        float: {},        
        Note: {
            'synth': Synth.play
        },
        type(None): {},
    }
    
    variables = {
        "bpm": 120
    }
    
    return Environment([ variables ], functions, methods)
 
