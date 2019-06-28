from enum import Enum

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
    
    def __str__(self):
        return "Program:\n" + "\n".join([str(e) for e in self.children])
    

class BlockNode(Node):
    def __init__(self):      
        Node.__init__(self)              
    
    def __str__(self):
        return "B{\n" + "\n".join([str(e) for e in self.children]) + "\n}"


class ListNode(Node):
    def __init__(self):
        Node.__init__(self)              
    
    def __str__(self):
        return "@(" + ", ".join([str(e) for e in self.children]) + ")"      
        
class IdentifierNode(Node):
    def __init__(self, identifier):        
        self.identifier = identifier
    
    def __str__(self):
        return f"L'{self.identifier}'"
        
class AssignExpression(Node):
    def __init__(self, target, value):        
        self.target = target
        self.value = value
        
    def __str__(self):
        return f"A[{self.target} = {self.value}]"
   
class AsteriskStatementNode(Node):
    def __init__(self, iterator, statement):        
        self.iterator = iterator
        self.statement = statement
        
    def __str__(self):
        return f"*({self.iterator}: {self.statement})"
   
class ColonNode(Node):
    def __init__(self, a, b):        
        self.a = a
        self.b = b
        
    def __str__(self):
        return f":({self.a}, {self.b})"
   
class ExpressionNode(Node):
    def __str__(self):
        return f"{self.__class__.__name__}('{self.value}')"


class IntegerLiteralNode(ExpressionNode):
    def __init__(self, value):        
        self.value = value        
    
    def __str__(self):
        return f"i'{self.value}'"

class StringLiteralNode(ExpressionNode):
    def __init__(self, value):        
        self.value = value

    def __str__(self):
        return f"s'{self.value}'"
    
class NoteLiteralNode(ExpressionNode):
    def __init__(self, value):        
        self.value = value
        
    def __str__(self):
        return f"n'{self.value.note}[{self.value.octave}, {self.value.duration}]'"

class FunctionCallNode(Node):
    def __init__(self, identifier, arguments):        
        self.identifier = identifier
        self.arguments = arguments
        
    def __str__(self):
        return f"F({self.identifier}: {self.arguments})"

class CommaNode(Node):    
    def __str__(self):
        return "[,]"

class PercentNode(Node):
    def __init__(self, value):        
        self.value = value
        
    def __str__(self):
        return f"%'{self.value}'"
