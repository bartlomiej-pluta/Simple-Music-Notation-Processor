from Tokenizer import *
from Note import *
from AST import *
from Error import SyntaxException

def expectedFound(expected, found):
    raise SyntaxException(None, f"Expected: {expected}, found: {found}")

def assertType(expected, found):
    if expected != found:
        raise SyntaxException(None, f"Expected: {expected}, found: {found}")

def parseInteger(input, parent):
    token = input.pop(0)
    return IntegerLiteralNode(int(token.value), parent, token.pos)
    
def parseString(input, parent):   
    token = input.pop(0)
    return StringLiteralNode(token.value[1:-1], parent, token.pos)
    
def parseNote(input, parent): 
    token = input.pop(0)
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
        if consumedChars < len(value) and value[consumedChars] == '.':
            dot = True
            consumedChars += 1
    
    return NoteLiteralNode(Note(notePitch, octave, duration, dot), parent, token.pos)

def parseComma(input, parent):
    token = input.pop(0)
    return CommaNode(parent, token.pos)

def parseList(input, parent):       
    token = input.pop(0)
    
    node = ListNode(parent, token.pos)
    
    while input[0].type != TokenType.CLOSE_PAREN:  
        element = parseArrayElement(input, node)
        if element is None:
            raise SyntaxException(input[0].pos, "Invalid element '{input[0].value}'")
        node.append(element)
    
    if input[0].type != TokenType.CLOSE_PAREN:
        expectedFound(TokenType.CLOSE_PAREN, input[0].type)
    input.pop(0)
    
    return node
            
def parseBlock(input, parent):
    token = input.pop(0)
    
    block = BlockNode(parent, token.pos)
    
    while input[0].type != TokenType.CLOSE_BRACKET:
        block.append(parseToken(input, block))
    
    if input[0].type != TokenType.CLOSE_BRACKET:
        expectedFound(TokenType.CLOSE_BRACKET, input[0].type)
    input.pop(0)
    
    return block


def parseAsterisk(input, parent):
    token = input.pop(0)
    
    iterator = parent.pop(-1)
    value = parseStatement(input, parent)
    
    asterisk = AsteriskStatementNode(iterator, value, parent, token.pos)        
    iterator.parent = asterisk
    value.parent = asterisk
    return asterisk
   
def parseNoteOrColon(input, parent):
    note = parseNote(input, parent)    
    if len(input) > 1 and input[0].type == TokenType.COLON:
        token = input.pop(0)                
        b = parseNote(input, parent)
        if b is None:
            raise SyntaxException(input[0].pos, f"Invalid colon argument '{input[0].value}'")
        colon = ColonNode(note, b, parent, token.pos)
        note.parent = colon
        b.parent = colon
        return colon
    
    return note
   
def parseIntegerOrColonOrPercent(input, parent):
    integer = parseInteger(input, parent)    
    if len(input) > 1 and input[0].type == TokenType.COLON:
        token = input.pop(0)                
        b = parseInteger(input, parent) 
        if b is None:
            raise SyntaxException(input[0].pos, f"Invalid colon argument '{input[0].value}'")
        colon = ColonNode(integer, b, parent, token.pos)
        integer.parent = colon
        b.parent = colon
        return colon
    
    if len(input) > 0 and input[0].type == TokenType.PERCENT:
        input.pop(0)
        percent = PercentNode(integer, parent, integer.pos)
        integer.parent = percent
        return percent
    
    return integer   
   
def parseFunctionCallOrAssignOrIdentifier(input, parent):   
    token = input.pop(0)
    identifier = IdentifierNode(token.value, parent, token.pos)
    # Function call
    if len(input) > 0 and input[0].type == TokenType.OPEN_PAREN:            
        arguments = parseList(input, parent)        
        func = FunctionCallNode(identifier, arguments, parent, token.pos)
        identifier.parent = func
        arguments.parent = func
        return func
    # Assign
    if len(input) > 1 and input[0].type == TokenType.ASSIGN:          
        token = input.pop(0)            
        value = parseExpression(input, parent) #
        assign = AssignExpression(identifier, value, parent, token.pos)
        identifier.parent = assign
        value.parent = assign
        return assign
        
    return identifier

def parseMinus(input, parent):
    token = input.pop(0)
    
    value = parseInteger(input, parent)
    
    return IntegerLiteralNode(-value.value, parent, token.pos)

def parseFunctionDefinition(input, parent):
    input.pop(0)
    
    assertType(TokenType.IDENTIFIER, input[0].type)
    token = input.pop(0)
    name = IdentifierNode(token.value, parent, token.pos)
    
    assertType(TokenType.OPEN_PAREN, input[0].type)
    parameters = parseList(input, parent)
    
    assertType(TokenType.OPEN_BRACKET, input[0].type)
    body = parseBlock(input, parent)
    
    func = FunctionDefinitionNode(name, parameters, body, parent, token.pos)
    name.parent = func
    parameters.parent = func
    body.parent = func
    return func

def parseReturn(input, parent):
    token = input.pop(0)
    
    value = parseExpression(input, parent)
    
    returnNode = ReturnNode(value, parent, token.pos)
    value.parent = returnNode
    return returnNode

def parseExpression(input, parent):    
    type = input[0].type
    if type == TokenType.FUNCTION:
        return parseFunctionDefinition(input, parent)
    if type == TokenType.RETURN:
        return parseReturn(input, parent)
    if type == TokenType.MINUS:
        return parseMinus(input, parent)
    if type == TokenType.INTEGER:
        return parseIntegerOrColonOrPercent(input, parent)
    if type == TokenType.STRING:
        return parseString(input, parent)    
    if type == TokenType.NOTE:
        return parseNoteOrColon(input, parent)    
    if type == TokenType.IDENTIFIER:
        return parseFunctionCallOrAssignOrIdentifier(input, parent)    
    if type == TokenType.OPEN_PAREN:
        return parseList(input, parent)     
    raise SyntaxException(input[0].pos, f"Unexpected character '{input[0].value}'")
 
def parseArrayElement(input, parent):
    type = input[0].type
    if type == TokenType.COMMA:
        return parseComma(input, parent)
    return parseExpression(input, parent)
 
def parseStatement(input, parent):
    type = input[0].type
    if type == TokenType.OPEN_BRACKET:
        return parseBlock(input, parent)
    if type == TokenType.ASTERISK:
        return parseAsterisk(input, parent)
    
    return parseExpression(input, parent)
    
def parseToken(input, parent):      
    #import pdb; pdb.set_trace()
    return parseStatement(input, parent)    
    
  
def parse(input):    
    root = Program()
    while len(input) > 0:
        root.append(parseToken(input, root))
    return root
