class SyntaxException(Exception):
    def __init__(self, pos, msg):        
        posStr = "" if pos is None else f"[line {pos[0]+1}, col {pos[1]+1}]"        
        self.msg = f"Syntax error {posStr}:\n{msg}"
    
class RuntimeException(Exception):
    def __init__(self, pos, msg):
        posStr = "" if pos is None else f"[line {pos[0]+1}, col {pos[1]+1}]"        
        self.msg = f"Syntax error {posStr}:\n{msg}"
