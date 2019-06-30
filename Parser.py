from Tokenizer import *
from Note import *
from AST import *
from Error import ParseError

def expectedFound(expected, found):
    raise ParseError(f"Expected: {expected}, found: {found}")

def parseInteger(input, parent):
    return IntegerLiteralNode(int(input.pop(0).value))
    
def parseString(input, parent):    
    return StringLiteralNode(input.pop(0).value[1:-1])
    
def parseNote(input, parent): 
    value = input.pop(0).value
    consumedChars = 1
    notePitch = value[consumedChars]
    consumedChars += 1
    octave = 4
    duration = 4
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
    
    return NoteLiteralNode(Note(notePitch, octave, duration))

def parseComma(input, parent):
    input.pop(0)
    return CommaNode()

def parseList(input, parent):       
    input.pop(0)
    
    node = ListNode()
    
    while input[0].type != TokenType.CLOSE_PAREN:  
        element = parseArrayElement(input, node)
        if element is None:
            raise ParseError(f"Line: {input[0].pos[0]+1}, col: {input[0].pos[1]+1}: Invalid element '{input[0].value}'")
        node.append(element)
    
    if input[0].type != TokenType.CLOSE_PAREN:
        expectedFound(TokenType.CLOSE_PAREN, input[0].type)
    input.pop(0)
    
    return node
            
def parseBlock(input, parent):
    input.pop(0)
    
    block = BlockNode()
    
    while input[0].type != TokenType.CLOSE_BRACKET:
        block.append(parseToken(input, block))
    
    if input[0].type != TokenType.CLOSE_BRACKET:
        expectedFound(TokenType.CLOSE_BRACKET, input[0].type)
    input.pop(0)
    
    return block


def parseAsterisk(input, parent):
    input.pop(0)
    
    iterator = parent.pop(-1)
    value = parseStatement(input, parent) #TODO: only statements! (?)
    
    return AsteriskStatementNode(iterator, value)        
   
def parseNoteOrColon(input, parent):
    note = parseNote(input, parent)    
    if len(input) > 1 and input[0].type == TokenType.COLON:
        input.pop(0)                
        b = parseNote(input, parent) #TODO: only expressions!
        if b is None:
            raise ParseError(f"Line {input[0].pos[0]+1}, col {input[0].pos[1]+1}: Invalid colon argument '{input[0].value}'")
        return ColonNode(note, b)
    
    return note
   
def parseIntegerOrColon(input, parent):
    integer = parseInteger(input, parent)    
    if len(input) > 1 and input[0].type == TokenType.COLON:
        input.pop(0)                
        b = parseInteger(input, parent) #TODO: only expressions!
        if b is None:
            raise ParseError(f"Line {input[0].pos[0]+1}, col {input[0].pos[1]+1}: Invalid colon argument '{input[0].value}'")
        return ColonNode(integer, b)
    
    return integer   
   
def parseFunctionCallOrAssignOrIdentifier(input, parent):    
    identifier = IdentifierNode(input.pop(0).value)
    # Function call
    if len(input) > 0 and input[0].type == TokenType.OPEN_PAREN:            
        arguments = parseList(input, parent)        
        return FunctionCallNode(identifier, arguments)
    # Assign
    if len(input) > 1 and input[0].type == TokenType.ASSIGN:          
        input.pop(0)            
        value = parseExpression(input, parent) #TODO: only expressions!
        return AssignExpression(identifier, value)
        
    return identifier

def parsePercent(input, parent):
    input.pop(0)
    
    value = parent.pop(-1)
    
    return PercentNode(value)

def parseMinus(input, parent):
    input.pop(0)
    
    value = parseInteger(input, parent)
    
    return IntegerLiteralNode(-value.value)

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
    raise ParseError(f"Line {input[0].pos[0]+1}, col {input[0].pos[1]+1}: Unexpected character '{input[0].value}'")
 
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

if __name__ == "__main__":      
    try:
        with open(sys.argv[1], 'r') as source:
            lines = [line.rstrip('\n') for line in source.readlines()]
            
        tokens = [token for token in tokenize(lines) if token.type != TokenType.COMMENT]
        
        ast = parse(tokens)
        
        print(ast)
    except TokenizerError as e:
        print(str(e))
        
    except ParseError as e:
        print(str(e))
    
