from AST import *
from Note import Note
from Error import RuntimeException

def evaluateProgram(program, environment):
    for node in program.children:
        evaluate(node, environment)

def evaluateInteger(integer, environment):    
    return integer.value

def evaluatePercent(percent, environment):
    return percent.value.value * 0.01

def evaluateIdentifier(identifier, environment):
    value = environment.findVariable(identifier.identifier)
    return value

def evaluateString(string, environment):    
    value = string.value    
    for scope in reversed(environment.scopes):
        for k, v in scope.items():
            value = value.replace('{' + k + '}', objectString(v)) #TODO: poprawic
    return value



def evaluateNote(note, environment):
    return note.value

def evaluateFunctionDefinition(definition, environment):
    name = definition.name
    params = list([p for p in flatListNode(definition.parameters) if not isinstance(p, CommaNode)])
    body = definition.body
    
    if not isinstance(definition.parent, Program):
        raise RuntimeException(name.pos, f"Functions can be defined only on the top level of script")
    
    for p in params:
        if not isinstance(p, IdentifierNode):
            raise RuntimeException(p.pos, "Parameter of function definition must be an identifier")
        
    if name.identifier in environment.customFunctions or name.identifier in environment.functions:
        raise RuntimeException(name.pos, f"Function '{name.identifier}' already exists")
    
    environment.customFunctions[name.identifier] = {
        'params': params,
        'body': flatListNode(body)
    }
    
def flatListNode(listNode):
    if len(listNode.children[0].children) == 1:
        return []
    return _flatListNode(listNode.children[0], [])

def _flatListNode(listItemNode, list = []):        
    if len(listItemNode.children) == 2:        
        child1 = listItemNode.children[0]    
        child2 = listItemNode.children[1]        
        list.append(child1)
        _flatListNode(child2, list)    
    return list

def evaluateAccess(access, environment):
    
    element = evaluate(access.element, environment)
    #TODO: narazie tylko metody działają        
    e = evaluateMethodCall(element, access.property, environment)
    return e
    
def evaluateMethodCall(element, functionCall, environment):
    funcName = functionCall.identifier.identifier
    arguments = evaluateList(functionCall.arguments, environment)
    arguments.insert(0, element)    
    #for name, function in environment.customFunctions.items():
        #if funcName == name:
            #if len(function['params']) != len(arguments):
                #raise RuntimeException(functionCall.pos, f"Calling '{funcName}' requires {len(function['params'])} and {len(arguments)} was passed")
            #environment.scopes.append({ function['params'][i].identifier: v for i, v in enumerate(arguments) })                      
            #returnValue = None            
            #for node in function['body']:                   
                #if not isinstance(node, ReturnNode):
                    #evaluate(node, environment)     
                #else:                    
                    #returnValue = evaluateReturn(node, environment)
            #environment.scopes.pop(-1)
            #return returnValue    
    for name, definition in environment.methods[type(element)].items():        
        if name == funcName:            
            return definition(arguments, environment)
    raise RuntimeException(functionCall.pos, f"Method '{funcName}' does not exist")

def evaluateFunctionCall(functionCall, environment):         
    funcName = functionCall.identifier.identifier
    arguments = evaluateList(functionCall.arguments, environment)       
    for name, function in environment.customFunctions.items():
        if funcName == name:
            if len(function['params']) != len(arguments):
                raise RuntimeException(functionCall.pos, f"Calling '{funcName}' requires {len(function['params'])} and {len(arguments)} was passed")
            environment.scopes.append({ function['params'][i].identifier: v for i, v in enumerate(arguments) })                      
            returnValue = None            
            for node in function['body']:                   
                if not isinstance(node, ReturnNode):
                    evaluate(node, environment)     
                else:                    
                    returnValue = evaluateReturn(node, environment)
            environment.scopes.pop(-1)
            return returnValue
    for name, definition in environment.functions.items():
        if name == funcName:
            return definition(arguments, environment)
    raise RuntimeException(functionCall.pos, f"Function '{funcName}' does not exist")
        
def evaluateReturn(returnNode, environment):
    return evaluate(returnNode.value, environment)

def evaluateComma(comma, environment):
    pass

def evaluateBlock(block, environment):
    environment.scopes.append({})
    for node in flatListNode(block):
        evaluate(node, environment)
    environment.scopes.pop(-1)

def evaluateList(list, environment):
    return [evaluate(e, environment) for e in flatListNode(list) if not isinstance(e, CommaNode)]    

def evaluateAssignment(assignment, environment):
    target = assignment.target.identifier
    value = evaluate(assignment.value, environment)
    scopeOfExistingVariable = environment.findVariableScope(target)
    if scopeOfExistingVariable is not None:
        scopeOfExistingVariable[target] = value
    else:
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
    if isinstance(colon.a, NoteLiteralNode) and isinstance(colon.b, NoteLiteralNode):
        return Note.range(colon.a.value, colon.b.value)
    elif isinstance(colon.a, IntegerLiteralNode) and isinstance(colon.b, IntegerLiteralNode):
        return list(range(colon.a.value, colon.b.value+1))
    raise RuntimeException(colon.pos, "Invalid colon arguments")

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
    if isinstance(input, FunctionDefinitionNode):
        return evaluateFunctionDefinition(input, environment)
    if isinstance(input, FunctionCallNode):
        return evaluateFunctionCall(input, environment)
    if isinstance(input, AccessNode):
        return evaluateAccess(input, environment)
    if isinstance(input, CommaNode):    
        return evaluateComma(input, environment)
    if isinstance(input, BlockNode):
        return evaluateBlock(input, environment)
    if isinstance(input, ListNode):
        return evaluateList(input, environment)
    if isinstance(input, AssignmentNode):
        return evaluateAssignment(input, environment)
    if isinstance(input, AsteriskNode):
        return evaluateAsterisk(input, environment)
    if isinstance(input, ColonNode):
        return evaluateColon(input, environment)
    if isinstance(input, IdentifierNode):
        return evaluateIdentifier(input, environment)
