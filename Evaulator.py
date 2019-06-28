from Tokenizer import tokenize, TokenType
from Parser import parse
from AST import *
import sys
from Note import *
import random

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
            value = value.replace('{' + k + '}', str(v))
    return value

def evaluateNote(note, environment):
    return note.value

def evaluateFunctionCall(functionCall, environment):       
    function = functionCall.identifier.identifier
    arguments = evaluateList(functionCall.arguments, environment)
    #TODO: example
    for name, definition in environment.functions.items():
        if name == function:
            return definition(arguments)
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
    for i in range(count):
        if isinstance(asterisk.iterator, IdentifierNode):
            environment.scopes[-1][f"_{asterisk.iterator.identifier}"] = i+1
        evaluate(asterisk.statement, environment)
    
def evaluateColon(colon, environment):
    if isinstance(colon.a, IntegerLiteralNode) and isinstance(colon.b, IntegerLiteralNode):
        return list(range(evaluateInteger(colon.a, environment), evaluateInteger(colon.b, environment)+1))
    if isinstance(colon.a, NoteLiteralNode) and isinstance(colon.b, NoteLiteralNode):
        return NotePitch.range(colon.a.value.note, colon.b.value.note)
    raise RuntimeException("Range can be created using only note or integer literals")

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
        

if __name__ == "__main__":
    
    functions = {
        'print': lambda args: print("".join([str(arg) for arg in args])),    
        'midi': lambda args: print(":".join([str(type(arg)) for arg in args])),
        'random': lambda args: args[0][int(random.uniform(0, len(args[0])))][1]
    }
    
    with open(sys.argv[1], 'r') as source:
        lines = [line.rstrip('\n') for line in source.readlines()]
            
    tokens = [token for token in tokenize(lines) if token.type != TokenType.COMMENT]
       
    ast = parse(tokens)            
    
    environment = Environment([{}], functions)
    evaluate(ast, environment)
    
