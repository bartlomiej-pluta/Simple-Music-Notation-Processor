import os
from Tokenizer import tokenize, TokenType
from Parser import parse
from AST import *
import sys
from Note import *
import random
import Midi

class RuntimeException(Exception):
    pass

class Environment():
    def __init__(self, scopes, functions):
        self.scopes = scopes
        self.functions = functions

def evaluateProgram(program, environment):
    for node in program.children:
        evaluate(node, environment)

def evaluateInteger(integer, environment):    
    return integer.value

def evaluatePercent(percent, environment):
    pass

def evaluateIdentifier(identifier, environment):
    value = findVariable(identifier.identifier, environment)
    return value

def findVariable(name, environment):        
    for scope in reversed(environment.scopes):
        if name in scope:
            return scope[name]
    raise RuntimeException(f"Variable '{name}' is not declared")

def evaluateString(string, environment):    
    value = string.value    
    for scope in reversed(environment.scopes):
        for k, v in scope.items():
            value = value.replace('{' + k + '}', objectString(v)) #TODO: poprawic
    return value

def evaluateNote(note, environment):
    return note.value

def evaluateFunctionCall(functionCall, environment):       
    function = functionCall.identifier.identifier
    arguments = evaluateList(functionCall.arguments, environment)    
    for name, definition in environment.functions.items():
        if name == function:
            return definition(arguments, environment)
    raise RuntimeException(f"Function '{function}' does not exist")
        

def evaluateComma(comma, environment):
    pass

def evaluateBlock(block, environment):
    environment.scopes.append({})
    for node in block.children:
        evaluate(node, environment)
    environment.scopes.pop(-1)

def evaluateList(list, environment):
    return [evaluate(e, environment) for e in list if not isinstance(e, CommaNode)]

def evaluateAssignment(assignment, environment):
    target = assignment.target.identifier
    value = evaluate(assignment.value, environment)
    environment.scopes[-1][target] = value

def evaluateAsterisk(asterisk, environment):    
    count = evaluate(asterisk.iterator, environment)
    if isinstance(count, int):
        for i in range(count):
            if isinstance(asterisk.iterator, IdentifierNode):
                environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = i+1
            else:
                environment.scopes[-1]["_"] = i+1
            evaluate(asterisk.statement, environment)
        if isinstance(asterisk.iterator, IdentifierNode):
            del environment.scopes[-1][f"_{asterisk.iterator.identifier}"]
        else: 
            environment.scopes[-1]["_"] = i+1
    elif isinstance(count, list):
        for i, v in enumerate(count):
            if isinstance(asterisk.iterator, IdentifierNode):
                environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = i+1
                environment.scopes[-1][f"{asterisk.iterator.identifier}_"] = v
            else:
                environment.scopes[-1]["_"] = i+1
                environment.scopes[-1]["__"] = v
            evaluate(asterisk.statement, environment)
            if isinstance(asterisk.iterator, IdentifierNode):
                del environment.scopes[-1][f"_{asterisk.iterator.identifier}"]
                del environment.scopes[-1][f"{asterisk.iterator.identifier}_"]
            else:
                del environment.scopes[-1]["_"]
                del environment.scopes[-1]["__"]
    
def evaluateColon(colon, environment):        
    return Note.range(colon.a.value, colon.b.value)

def evaluate(input, environment):
    if isinstance(input, Program):
        return evaluateProgram(input, environment)
    if isinstance(input, IntegerLiteralNode):
        return evaluateInteger(input, environment)
    if isinstance(input, PercentNode):
        return evaluatePercent(input, environment)
    if isinstance(input, StringLiteralNode):
        return evaluateString(input, environment)
    if isinstance(input, NoteLiteralNode):
        return evaluateNote(input, environment)
    if isinstance(input, FunctionCallNode):
        return evaluateFunctionCall(input, environment)
    if isinstance(input, CommaNode):
        return evaluateComma(input, environment)
    if isinstance(input, BlockNode):
        return evaluateBlock(input, environment)
    if isinstance(input, ListNode):
        return evaluateList(input, environment)
    if isinstance(input, AssignExpression):
        return evaluateAssignment(input, environment)
    if isinstance(input, AsteriskStatementNode):
        return evaluateAsterisk(input, environment)
    if isinstance(input, ColonNode):
        return evaluateColon(input, environment)
    if isinstance(input, IdentifierNode):
        return evaluateIdentifier(input, environment)
  
def rand(args, env):
    if len(args) == 1 and isinstance(args[0], list):
        return args[0][int(random.uniform(0, len(args[0])))]

def objectString(obj):    
    if isinstance(obj, str):
        return obj
    if isinstance(obj, int):       
        return str(obj)
    if isinstance(obj, Note):
        return obj.note.name
    if isinstance(obj, list):
        return "(" + ", ".join([objectString(v) for v in obj]) + ")"
    raise RuntimeException(f"Don't know how to interpret {str(obj)}")
 
def prt(args, env):
    print("".join([objectString(arg) for arg in args]))

def semitonesList(list):
    withoutPauses = tuple(filter(lambda x: isinstance(x, Note), list))    
    r = [Note.checkInterval(withoutPauses[i-1], withoutPauses[i]) for i, _ in enumerate(withoutPauses) if i != 0]
    return r[0] if len(r) == 1 else r

def semitones(args, env):
    if len(args) > 0 and isinstance(args[0], list):
        return semitonesList(args[0])
    return semitonesList(args)

def intervalList(list):    
    r = [intervalToString(x) for x in list]
    return r[0] if len(r) == 1 else r

def interval(args, env):    
    if len(args) > 0 and isinstance(args[0], list):        
        return intervalList(args[0])
    return intervalList(args)
 
def transpose(args, env):
    if len(args) > 1 and isinstance(args[0], int):
        value = args[0]
        transposed = []
        for i, arg in enumerate(args):            
            if i == 0:
                continue
            if not isinstance(arg, list):
                return # is not list            
            transposed.append([note.transpose(value) for note in arg if isinstance(note, Note)])
        return transposed
    else:
        return # not valid signature
 
if __name__ == "__main__":            
    functions = {
        'print': prt,
        'midi': Midi.play,
        'pause': Midi.pause,
        'type': lambda args, env: print(type(args[0])),
        'random': rand,
        'semitones': semitones,
        'interval': interval,
        'transpose': transpose
        
    }
    
    with open(sys.argv[1], 'r') as source:
        lines = [line.rstrip('\n') for line in source.readlines()]
            
    tokens = [token for token in tokenize(lines) if token.type != TokenType.COMMENT]
       
    ast = parse(tokens)                
    environment = Environment([{ "bpm": 120 }], functions)
    evaluate(ast, environment)
    
