from AST import *
from Tokenizer import TokenType
from Error import SyntaxException

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
        node.append(item)
        listTail = parseListTail(input, item)
        item.append(listTail)
        
        #while input.current().type != TokenType.CLOSE_PAREN:                        
            #elem = parseListTail(input, node)            
            #if elem is None:
                #raise SyntaxException(input.current().pos, f"Invalid element '{input.current().value}'")
            #node.append(elem)
        return node
    return None
            

# listTail -> COMMA expr listTail | CLOSE_PAREN
def parseListTail(input, parent):        
    # listTail -> CLOSE_PAREN
    if input.current().type == TokenType.CLOSE_PAREN:   
        close = CloseListNode(parent, input.current().pos)
        input.ahead()
        return close
    
    assertToken(TokenType.COMMA, input)
    input.ahead()
        
    expr = parseExpression(input, parent)        
    if expr is not None: 
        item = ListItemNode(expr, parent, expr.pos)            
        expr.parent = item           
        listTail = parseListTail(input, item)
        item.append(listTail)
        listTail.parent = item
        input.ahead()
        return item
    
    return None

def parseExpression(input, parent):
    value = runParsers(input, parent, [
        parseInteger,
        parseList        
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






def parseNote(input, parent):
    pass
