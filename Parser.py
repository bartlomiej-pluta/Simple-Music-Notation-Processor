from AST import *
from Tokenizer import TokenType
from Error import SyntaxException
from Note import Note, NotePitch
import re

def assertToken(expected, input):    
    if not input.hasCurrent():
        raise SyntaxException(None, f"Expected '{expected}'")    
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
        integer = IntegerLiteralNode(int(input.current().value), parent, input.current().pos)
        input.ahead()
        
        return integer
    return None

# percent -> int '%'
def parseIntegerAndPercent(input, parent):       
    integer = parseInteger(input, parent)        
    if integer is not None and input.hasCurrent() and input.current().type == TokenType.PERCENT:
        percent = PercentNode(integer, parent, input.current().pos)
        integer.parent = percent
        input.ahead()
        
        return percent
    return integer

# string -> STRING
def parseString(input, parent):
    if input.current().type == TokenType.STRING:
        string = StringLiteralNode(input.current().value[1:len(input.current().value)-1], parent, input.current().pos)
        input.ahead()
        
        return string
    return None

# id -> IDENTIFIER
def parseIdentifier(input, parent):
    if input.current().type == TokenType.IDENTIFIER:
        identifier = IdentifierNode(input.current().value, parent, input.current().pos)
        input.ahead()
        
        return identifier
    return None

def parseIdentifierOrFunctionCallOrAssignment(input, parent):
    identifier = parseIdentifier(input, parent)
    if identifier is not None and input.hasCurrent():
        if input.current().type == TokenType.ASSIGN:
            token = input.current()
            input.ahead()
            
            expr = parseExpression(input, parent)
            
            assignment = AssignmentNode(identifier, expr, parent, token.pos)
            identifier.parent = assignment
            expr.parent = assignment
                        
            return assignment
        
        args = parseList(input, parent)
        if args is not None:
            functionCall = FunctionCallNode(identifier, args, parent, identifier.pos)
            args.parent = functionCall
            identifier.parent = functionCall
            return functionCall
        
    return identifier

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
        if input.hasCurrent() and input.current().type == TokenType.CLOSE_PAREN:
            close = CloseListNode(node, input.current().pos)
            node.append(close)
            input.ahead()
            return node                
        
        # list -> expr listTail
        if input.hasCurrent():
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
    if input.hasCurrent() and input.current().type == TokenType.CLOSE_PAREN:   
        close = CloseListNode(parent, input.current().pos)
        input.ahead()
        return close
    
    # listTail -> COMMA expr listTail
    if input.hasCurrent() and input.hasMore():        
        assertToken(TokenType.COMMA, input)
        input.ahead()
        expr = rollup(parseExpression)(input, parent)        
        if expr is not None: 
            item = ListItemNode(expr, parent, expr.pos)            
            expr.parent = item           
            listTail = parseListTail(input, item)
            item.append(listTail)        
            listTail.parent = item        
            return item
    
    return None

# colon -> expr ':' expr
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

# minus -> '-' int
def parseMinus(input, parent):
    if input.current().type == TokenType.MINUS:
        token = input.current()
        input.ahead()
        
        expr = parseInteger(input, parent)        
        
        return IntegerLiteralNode(-expr.value, parent, token.pos)


# block -> '{' '}' | '{' blockItem
def parseBlock(input, parent):      
    # '{'
    if input.current().type == TokenType.OPEN_BRACKET:
        token = input.current()
        input.ahead()
        
        node = BlockNode(parent, token.pos)        
        
        # '}'
        if input.hasCurrent() and input.current().type == TokenType.CLOSE_BRACKET:
            input.ahead()
            return node
        
        # blockItem
        if input.hasCurrent():
            item = parseBlockItem(input, node)
            node.append(item)
            return node
        
    return None
          
# blockItem -> stmt | '}'          
def parseBlockItem(input, parent):      
    # '}'    
    if input.hasCurrent() and input.current().type == TokenType.CLOSE_BRACKET:
        close = CloseBlockNode(parent, input.current().pos)
        input.ahead()
        return close
    
    if input.hasCurrent():        
        stmt = parseStatement(input, parent)
        
        if stmt is not None:
            item = BlockItemNode(stmt, parent, stmt.pos)
            stmt.parent = item
            nextBlockItem = parseBlockItem(input, item)
            if nextBlockItem != None:
                item.append(nextBlockItem)
            return item
        
    return None

def rollup(parser):
    def _rollup(input, parent):
        node = Node(None, (-1, -1))
        elem = parser(input, node)
        while elem is not None:
            node.append(elem)            
            elem = parser(input, node)
        return node.children[0] if len(node.children) > 0 else None
    return _rollup
    
def parseFunctionDefinition(input, parent):
    if input.current().type == TokenType.FUNCTION:
        token = input.current()
        input.ahead()
        
        assertToken(TokenType.IDENTIFIER, input)
        identifier = parseIdentifier(input, parent)
        
        assertToken(TokenType.OPEN_PAREN, input)
        args = parseList(input, parent)
        
        assertToken(TokenType.OPEN_BRACKET, input)
        body = parseBlock(input, parent)
        
        function = FunctionDefinitionNode(identifier, args, body, parent, token.pos)
        identifier.parent = function
        args.parent = function
        body.parent = function
        
        return function
    return None

def parseReturn(input, parent):
    if input.current().type == TokenType.RETURN:
        token = input.current()
        input.ahead()
        
        expr = parseExpression(input, parent)
        
        node = ReturnNode(expr, parent, token.pos)
        expr.parent = node
        
        return node
    return None

def parseStatement(input, parent):
    stmt = runParsers(input, parent, [        
        parseBlock,
        parseExpression,
        parseFunctionDefinition,
        parseReturn
    ])    

    asterisk = parseAsterisk(stmt, input, parent)
    if asterisk is not None:
        return asterisk

    return stmt

# asterisk -> expr '*' stmt
def parseAsterisk(expr, input, parent):
    if input.hasMore() and input.current().type == TokenType.ASTERISK:                
        token = input.current()
        input.ahead()
        
        stmt = parseStatement(input, parent)
        
        asterisk = AsteriskNode(expr, stmt, parent, token.pos)
        expr.parent = asterisk
        stmt.parent = asterisk
        return asterisk
    return None

def parseExpression(input, parent):
    expr = runParsers(input, parent, [
        parseIntegerAndPercent,
        parseMinus,
        parseString,
        parseNote,        
        parseList, 
        parseIdentifierOrFunctionCallOrAssignment,
    ])    
    
    colon = parseColon(expr, input, parent)
    if colon is not None:
        return colon        
    
    return expr

# colon -> expr ':' expr
def parseColon(expr1, input, parent):
    if input.hasCurrent() and input.current().type == TokenType.COLON:
        token = input.current()
        input.ahead()
        expr2 = parseExpression(input, parent)
        
        if expr2 is None:
            raise SyntaxException(input.current().pos, f"Expected expression '{input.current().value}'")
        colon = ColonNode(expr1, expr2, parent, token.pos)
        expr1.parent = colon
        expr2.parent = colon
        return colon
    return None

def parseToken(input, parent):    
    value = runParsers(input, parent, [
        parseStatement        
    ])        
       
    if value is None:
        raise SyntaxException(None, "Unknown statement") #TODO
    
    return value

def parse(input):
    root = Program()
    while input.hasCurrent():
        root.append(parseToken(input, root))    
    return root
