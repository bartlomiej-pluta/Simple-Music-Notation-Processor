from AST import *
from Tokenizer import TokenType
from Error import SyntaxException
from Note import Note, NotePitch
import re

def assertToken(expected, input):
    if expected != input.current().type:
        raise SyntaxException(input.current().pos, f"Expected '{expected}', found '{input.current().value}'")

def runParsers(input, parent, parsers):
    for parser in parsers:
        value = parser(input, parent)
        if value is not None:
            return value
    return None

def returnAndGoAhead(input, getValue):
    value = getValue(input.current())
    input.ahead()
    return value

# int -> INTEGER
def parseInteger(input, parent):    
    if input.current().type == TokenType.INTEGER:
        integer = IntegerLiteralNode(input.current().value, parent, input.current().pos)
        input.ahead()
        
        return integer
    return None

# string -> STRING
def parseString(input, parent):
    if input.current().type == TokenType.STRING:
        string = StringLiteralNode(input.current().value[1:len(input.current().value)-1], parent, input.current().pos)
        input.ahead()
        
        return string
    return None

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
            if consumedChars < len(value) and value[consumedChars] == '.':
                dot = True
                consumedChars += 1
        
        input.ahead()
        return NoteLiteralNode(Note(notePitch, octave, duration, dot), parent, token.pos)
    return None

# list -> CLOSE_PAREN | expr listTail
def parseList(input, parent):          
    if input.current().type == TokenType.OPEN_PAREN:
        node = ListNode(parent, input.current().pos)                
        input.ahead()
        
        # list -> CLOSE_PAREN (end of list)
        if input.current().type == TokenType.CLOSE_PAREN:
            close = CloseListNode(node, input.current().pos)
            node.append(close)
            input.ahead()
            return node                
        
        # list -> expr listTail
        token = input.current()
        expr = parseExpression(input, node)
        item = ListItemNode(expr, node, token.pos)
        expr.parent = item
        node.append(item)
        listTail = parseListTail(input, item)
        item.append(listTail)        
        return node
    return None
            

# listTail -> COMMA expr listTail | CLOSE_PAREN
def parseListTail(input, parent):         
    # listTail -> CLOSE_PAREN
    if input.current().type == TokenType.CLOSE_PAREN:   
        close = CloseListNode(parent, input.current().pos)
        input.ahead()
        return close
    
    # listTail -> COMMA expr listTail
    assertToken(TokenType.COMMA, input)
    input.ahead()
    expr = parseExpression(input, parent)        
    if expr is not None: 
        item = ListItemNode(expr, parent, expr.pos)            
        expr.parent = item           
        listTail = parseListTail(input, item)
        item.append(listTail)        
        listTail.parent = item        
        return item
    
    return None

def parseColon(input, parent):          
    if input.hasMore() and input.current().type == TokenType.COLON:
        expr1 = parent.pop(-1)
        
        token = input.current()
        input.ahead()           
        
        expr2 = parseExpression(input, parent)
        
        colon = ColonNode(expr1, expr2, parent, token.pos)
        expr1.parent = colon
        expr2.parent = colon
        return colon
    return None

def parseExpression(input, parent):
    value = runParsers(input, parent, [
        parseInteger,
        parseString,
        parseNote,
        parseList,      
        parseColon,
    ])
    
    if value is None:
        raise SyntaxException(input.current().pos, f"Expression expected")
    
    return value
    

def parseToken(input, parent):
    value = runParsers(input, parent, [
        parseExpression
    ])
    
    if value is None:
        raise SyntaxException(input.current().pos, "Unknown statement")
    
    return value

def parse(input):
    root = Program()
    while input.notParsedTokensRemain():
        root.append(parseToken(input, root))    
    return root
