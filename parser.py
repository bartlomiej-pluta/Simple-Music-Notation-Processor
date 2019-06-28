from enum import Enum
from tokenizer import *
from note import *
import json

class ParseError(Exception):
    pass

class NodeType(Enum):
    INTEGER = 1
    STRING = 2
    NOTE = 3
    BLOCK = 4
    ARGUMENTS = 5
    IDENTIFIER = 6
    ASSIGN = 7
    PROGRAM = 8
    ASTERISK = 9
    COLON = 10
    FUNCTION_CALL = 11
    COMMA = 12
    PERCENT = 13

class Node:
    def __init__(self):
        self.children = []            
        
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.children)
        
    def __getitem__(self, index):
        return self.children[index]
  
    def append(self, node):
        self.children.append(node)
        
    def pop(self, index):
        return self.children.pop(index)

class Program(Node):
    def __init__(self):
        Node.__init__(self)
        self.type =  NodeType.PROGRAM        
    
    def __str__(self):
        return "Program:\n" + "\n".join([str(e) for e in self.children])
    

class BlockNode(Node):
    def __init__(self):      
        Node.__init__(self)
        self.type = NodeType.BLOCK        
    
    def __str__(self):
        return "B{\n" + "\n".join([str(e) for e in self.children]) + "\n}"


class ArgumentsNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.type = NodeType.ARGUMENTS        
    
    def __str__(self):
        return "@(" + ", ".join([str(e) for e in self.children]) + ")"      
        
class IdentifierNode(Node):
    def __init__(self, identifier):
        self.type = NodeType.IDENTIFIER
        self.identifier = identifier
    
    def __str__(self):
        return f"L'{self.identifier}'"
        
class AssignExpression(Node):
    def __init__(self, target, value):
        self.type = NodeType.ASSIGN
        self.target = target
        self.value = value
        
    def __str__(self):
        return f"A[{self.target} = {self.value}]"
   
class AsteriskStatementNode(Node):
    def __init__(self, iterator, statement):
        self.type = NodeType.ASTERISK
        self.iterator = iterator
        self.statement = statement
        
    def __str__(self):
        return f"*({self.iterator}: {self.statement})"
   
class ColonNode(Node):
    def __init__(self, a, b):
        self.type = NodeType.COLON
        self.a = a
        self.b = b
        
    def __str__(self):
        return f":({self.a}, {self.b})"
   
class ExpressionNode(Node):
    def __str__(self):
        return f"{self.__class__.__name__}('{self.value}')"


class IntegerLiteralNode(ExpressionNode):
    def __init__(self, value):
        self.type = NodeType.INTEGER
        self.value = value        
    
    def __str__(self):
        return f"i'{self.value}'"

class StringLiteralNode(ExpressionNode):
    def __init__(self, value):
        self.type = NodeType.STRING
        self.value = value

    def __str__(self):
        return f"s'{self.value}'"
    
class NoteLiteralNode(ExpressionNode):
    def __init__(self, value):
        self.type = NodeType.NOTE
        self.value = value
        
    def __str__(self):
        return f"n'{self.value}'"

class FunctionCallNode(Node):
    def __init__(self, identifier, arguments):
        self.type = NodeType.FUNCTION_CALL
        self.identifier = identifier
        self.arguments = arguments
        
    def __str__(self):
        return f"F({self.identifier}: {self.arguments})"

class CommaNode(Node):
    def __init__(self):
        self.type = NodeType.COMMA
        
    def __str__(self):
        return "[,]"

class PercentNode(Node):
    def __init__(self, value):
        self.type = NodeType.PERCENT
        self.value = value
        
    def __str__(self):
        return f"%'{self.value}'"

def expectedFound(expected, found):
    raise ParseError(f"Expected: {expected}, found: {found}")

def parseInteger(input, parent):
    if input[0].type != TokenType.INTEGER:
        expectedFound(TokenType.INTEGER, input[0].type)
    
    return IntegerLiteralNode(int(input.pop(0).value))
    
def parseString(input, parent):
    if input[0].type != TokenType.STRING:
        expectedFound(TokenType.STRING, input[0].type)
        
    return StringLiteralNode(input.pop(0).value[1:-1])
    
def parseNote(input, parent):
    if input[0].type != TokenType.NOTE:
        expectedFound(TokenType.NOTE, input[0].type)
    
    value = input.pop(0).value
    consumedChars = 1
    notePitch = value[consumedChars]
    consumedChars += 1
    octave = 1
    duration = 1
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
    if input[0].type != TokenType.COMMA:
        expectedFound(TokenType.COMMA, input[0].type)
    input.pop(0)
    return CommaNode()

def parseArguments(input, parent):    
    if input[0].type != TokenType.OPEN_PAREN:
        expectedFound(TokenType.OPEN_PAREN, input[0].type)
        
    input.pop(0)
    
    arguments = ArgumentsNode()
    
    while input[0].type != TokenType.CLOSE_PAREN:  
        arguments.append(parseArrayElement(input, arguments)) #TODO: parseExpression
    
    if input[0].type != TokenType.CLOSE_PAREN:
        expectedFound(TokenType.CLOSE_PAREN, input[0].type)
    input.pop(0)
    
    return arguments
            
def parseBlock(input, parent):
    if input[0].type != TokenType.OPEN_BRACKET:
        expectedFound(TokenType.OPEN_BRACKET, input[0].type)
        
    input.pop(0)
    
    block = BlockNode()
    
    while input[0].type != TokenType.CLOSE_BRACKET:
        block.append(parseToken(input, block))
    
    if input[0].type != TokenType.CLOSE_BRACKET:
        expectedFound(TokenType.CLOSE_BRACKET, input[0].type)
    input.pop(0)
    
    return block

def parseIdentifier(input, parent):
    if input[0].type != TokenType.IDENTIFIER:
        expectedFound(TokenType.IDENTIFIER, input[0].type)
    
    return IdentifierNode(input.pop(0).value)

def parseAssign(input, parent):
    if input[0].type != TokenType.ASSIGN:
        expectedFound(TokenType.ASSIGN, input[0].type)
        
    input.pop(0)
    
    target = parent.pop(-1)
    value = parseExpression(input, parent) #TODO: only expressions!
    
    return AssignExpression(target, value)

def parseAsterisk(input, parent):
    if input[0].type != TokenType.ASTERISK:
        expectedFound(TokenType.ASTERISK, input[0].type)
        
    input.pop(0)
    
    iterator = parent.pop(-1)
    value = parseStatement(input, parent) #TODO: only statements! (?)
    
    return AsteriskStatementNode(iterator, value)        
   
def parseColon(input, parent):    
    if input[0].type != TokenType.COLON:
        expectedFound(TokenType.COLON, input[0].type)
    
    input.pop(0)
    
    a = parent.pop(-1)
    b = parseExpression(input, parent) #TODO: only expressions!
    
    return ColonNode(a, b)
   
def parseFunctionCallOrIdentifier(input, parent):
    if input[0].type != TokenType.IDENTIFIER:
        expectedFound(TokenType.IDENTIFIER, input[0].type)
    
    if input[1].type == TokenType.OPEN_PAREN:
        identifier = parseIdentifier(input, parent)
        arguments = parseArguments(input, parent)        
        return FunctionCallNode(identifier, arguments)
    
    return parseIdentifier(input, parent)

def parsePercent(input, parent):
    if input[0].type != TokenType.PERCENT:
        expectedFound(TokenType.PERCENT, input[0].type)
        
    input.pop(0)
    
    value = parent.pop(-1)
    
    return PercentNode(value)

def parseExpression(input, parent):
    type = input[0].type
    if type == TokenType.INTEGER:
        return parseInteger(input, parent)
    if type == TokenType.STRING:
        return parseString(input, parent)
    if type == TokenType.NOTE:
        return parseNote(input, parent)    
    if type == TokenType.IDENTIFIER:
        return parseFunctionCallOrIdentifier(input, parent)
    if type == TokenType.PERCENT:
        return parsePercent(input, parent)
    if type == TokenType.OPEN_PAREN:
        return parseArguments(input, parent)
    if type == TokenType.ASSIGN:
        return parseAssign(input, parent)
    if type == TokenType.COLON:
        return parseColon(input, parent)    
 
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
    type = input[0].type    
    
    return parseStatement(input, parent)
    
  
def parseProgram(input):    
    root = Program()
    while len(input) > 0:
        root.append(parseToken(input, root))
    return root
  
def test():
    try:
        with open('test2.lit', 'r') as source:
            lines = [line.rstrip('\n') for line in source.readlines()]
            
        tokens = [token for token in tokenize(lines) if token.type != TokenType.COMMENT]
        
        ast = parseProgram(tokens)
        
        print(ast)
    except TokenizerError as e:
        print(str(e))
        
    except ParseError as e:
        print(str(e))
  
if __name__ == "__main__":      
    test()
    
