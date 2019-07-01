from Tokenizer import *
from Note import *
from AST import *
from Error import SyntaxException

def expectedFound(expected, found):
    raise SyntaxException(None, f"Expected: {expected}, found: {found}")

def parseInteger(input, parent):
    token = input.pop(0)
    return IntegerLiteralNode(int(token.value), token.pos)
    
def parseString(input, parent):   
    token = input.pop(0)
    return StringLiteralNode(token.value[1:-1], token.pos)
    
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
    
    return NoteLiteralNode(Note(notePitch, octave, duration, dot), token.pos)

def parseComma(input, parent):
    token = input.pop(0)
    return CommaNode(token.pos)

def parseList(input, parent):       
    token = input.pop(0)
    
    node = ListNode(token.pos)
    
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
    
    block = BlockNode(token.pos)
    
    while input[0].type != TokenType.CLOSE_BRACKET:
        block.append(parseToken(input, block))
    
    if input[0].type != TokenType.CLOSE_BRACKET:
        expectedFound(TokenType.CLOSE_BRACKET, input[0].type)
    input.pop(0)
    
    return block


def parseAsterisk(input, parent):
    token = input.pop(0)
    
    iterator = parent.pop(-1)
    value = parseStatement(input, parent) #TODO: only statements! (?)
    
    return AsteriskStatementNode(iterator, value, token.pos)        
   
def parseNoteOrColon(input, parent):
    note = parseNote(input, parent)    
    if len(input) > 1 and input[0].type == TokenType.COLON:
        token = input.pop(0)                
        b = parseNote(input, parent) #TODO: only expressions!
        if b is None:
            raise SyntaxException(input[0].pos, f"Invalid colon argument '{input[0].value}'")
        return ColonNode(note, b, token.pos)
    
    return note
   
def parseIntegerOrColon(input, parent):
    integer = parseInteger(input, parent)    
    if len(input) > 1 and input[0].type == TokenType.COLON:
        token = input.pop(0)                
        b = parseInteger(input, parent) #TODO: only expressions!
        if b is None:
            raise SyntaxException(input[0].pos, f"Invalid colon argument '{input[0].value}'")
        return ColonNode(integer, b, token.pos)
    
    return integer   
   
def parseFunctionCallOrAssignOrIdentifier(input, parent):   
    token = input.pop(0)
    identifier = IdentifierNode(token.value, token.pos)
    # Function call
    if len(input) > 0 and input[0].type == TokenType.OPEN_PAREN:            
        arguments = parseList(input, parent)        
        return FunctionCallNode(identifier, arguments, token.pos)
    # Assign
    if len(input) > 1 and input[0].type == TokenType.ASSIGN:          
        token = input.pop(0)            
        value = parseExpression(input, parent) #TODO: only expressions!
        return AssignExpression(identifier, value, token.pos)
        
    return identifier

def parsePercent(input, parent):
    token = input.pop(0)
    
    value = parent.pop(-1)
    
    return PercentNode(value, token.pos)

def parseMinus(input, parent):
    token = input.pop(0)
    
    value = parseInteger(input, parent)
    
    return IntegerLiteralNode(-value.value, token.pos)

def parseExpression(input, parent):    
    type = input[0].type
    if type == TokenType.MINUS:
        return parseMinus(input, parent)
    if type == TokenType.INTEGER:
        return parseIntegerOrColon(input, parent)
    if type == TokenType.STRING:
        return parseString(input, parent)    
    if type == TokenType.NOTE:
        return parseNoteOrColon(input, parent)    
    if type == TokenType.IDENTIFIER:
        return parseFunctionCallOrAssignOrIdentifier(input, parent)
    if type == TokenType.PERCENT:
        return parsePercent(input, parent)
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
