from enum import Enum
from Note import Note

class Node:
    def __init__(self, parent, pos):
        self.children = []
        self.parent = parent
        self.pos = pos
        for child in self.children:
            child.parent = self
        
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.children)
        
    def __getitem__(self, index):
        return self.children[index]        
    
    def append(self, node):
        node.parent = self
        self.children.append(node)
        
    def pop(self, index):
        return self.children.pop(index)
    
    def _print(self, level):        
        string = f"{pad(level)}{self.__class__.__name__}({self.parent.__class__.__name__}):\n"
        for child in self.children:
            if isinstance(child, str) or isinstance(child, int) or isinstance(child, Note):
                string += pad(level+1) + f"'{child}'\n"
            else:
                string += child._print(level+1)
        return string
    
    def __str__(self):
        return self._print(0)
    
def pad(level):
    return ("   " * level)

class Program(Node):
    def __init__(self):
        Node.__init__(self, None, (-1, -1))        
    
    #def __str__(self):
        #return "Program:\n" + "\n".join([str(e) for e in self.children])
    
    def print(self):
        print(self._print(0))

class BlockNode(Node):
    def __init__(self, parent, pos):      
        Node.__init__(self, parent, pos)              
    
    #def __str__(self):
        #return "B{\n" + "\n".join([str(e) for e in self.children]) + "\n}"

class BlockItemNode(Node):
    def __init__(self, statement, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.append(statement)
        self.statement = self.children[0]

class CloseBlockNode(Node):
    def __init__(self, parent, pos):
        Node.__init__(self, parent, pos)

class ListNode(Node):
    def __init__(self, parent, pos):
        Node.__init__(self, parent, pos)              
    
    #def __str__(self):
        #return "@(" + ", ".join([str(e) for e in self.children]) + ")"      
        
class IdentifierNode(Node):
    def __init__(self, identifier, parent, pos): 
        Node.__init__(self, parent, pos)   
        self.children.append(identifier)
        
        self.identifier = self.children[0]
    
    #def __str__(self):
        #return f"L'{self.identifier}'"
        
class AssignExpression(Node):
    def __init__(self, target, value, parent, pos):
        Node.__init__(self, parent, pos)     
        self.children.extend([target, value])
        
        self.target = self.children[0]
        self.value = self.children[1]
        
    #def __str__(self):
        #return f"A[{self.target} = {self.value}]"
   
class AsteriskNode(Node):
    def __init__(self, iterator, statement, parent, pos):
        Node.__init__(self, parent, pos)  
        self.children.extend([iterator, statement])
        
        self.iterator = self.children[0]
        self.statement = self.children[1]
        
    #def __str__(self):
        #return f"*({self.iterator}: {self.statement})"
   
class ColonNode(Node):
    def __init__(self, a, b, parent, pos):
        Node.__init__(self, parent, pos) 
        self.children.extend([a, b])
        
        self.a = self.children[0]
        self.b = self.children[1]
        
    #def __str__(self):
        #return f":({self.a}, {self.b})"
   
class ExpressionNode(Node):
    def __init__(self, parent, pos):
        Node.__init__(self, parent, pos)   
        
    #def __str__(self):
        #return f"{self.__class__.__name__}('{self.value}')"

class IntegerLiteralNode(ExpressionNode):
    def __init__(self, value, parent, pos):
        Node.__init__(self, parent, pos)   
        self.children.append(value)
        
        self.value = self.children[0]
    
    #def __str__(self):
        #return f"i'{self.value}'"

class StringLiteralNode(ExpressionNode):
    def __init__(self, value, parent, pos):
        Node.__init__(self, parent, pos)   
        self.children.append(value)
        
        self.value = self.children[0]

    #def __str__(self):
        #return f"s'{self.value}'"
    
class NoteLiteralNode(ExpressionNode):
    def __init__(self, value, parent, pos):
        Node.__init__(self, parent, pos)   
        self.children.append(value)
        
        self.value = self.children[0]
        
    #def __str__(self):
        #return f"n'{self.value.note}[{self.value.octave}, {self.value.duration}]'"

class FunctionCallNode(Node):
    def __init__(self, identifier, arguments, parent, pos):
        Node.__init__(self, parent, pos)  
        self.children.extend([identifier, arguments])
        
        self.identifier = self.children[0]
        self.arguments = self.children[1]
        
    #def __str__(self):
        #return f"F({self.identifier}: {self.arguments})"

class CommaNode(Node):    
    def __init__(self, parent, pos):
        Node.__init__(self, parent, pos)   
        
    #def __str__(self):
        #return "[,]"

class PercentNode(Node):
    def __init__(self, value, parent, pos):        
        Node.__init__(self, parent, pos)   
        self.children.append(value)
        
        self.value = self.children[0]
        
    #def __str__(self):
        #return f"%'{self.value}'"

class FunctionDefinitionNode(Node):
    def __init__(self, name, parameters, body, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.extend([name, parameters, body])
        
        self.name = self.children[0]
        self.parameters = self.children[1]
        self.body = self.children[2]
    
    #def __str__(self):
        #return f"$F'{self.name}{self.parameters}{self.body}"
    
class ReturnNode(Node):
    def __init__(self, value, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.append(value)
        
        self.value = self.children[0]
    
    #def __str__(self):
        #return f"Ret({self.value})"
    
class ListItemNode(Node):
    def __init__(self, value, parent, pos):
        Node.__init__(self, parent, pos)
        self.children.append(value)
        
        self.value = self.children[0]
        
class CloseListNode(Node):
    pass
