class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value    
        self.pos = pos
    def __str__(self):
        return "Token(" + str(self.type) + ", '" + self.value + "', " + str(self.pos) + ")"
    def __repr__(self):
        return self.__str__()

class TokenList:
    def __init__(self, tokens = []):
        self.tokens = tokens
        self.cursor = 0
        self.snap = 0
        
    def append(self, token):
        self.tokens.append(token)
        
    def __getitem__(self, index):
        return self.tokens[index]
    
    def current(self):
        if self.cursor >= len(self.tokens):
            raise RuntimeError(f"Cursor points to not existing token! Cursor = {self.cursor}, len = {len(self.tokens)}")
        return self.tokens[self.cursor]
    
    def next(self, number=1):
        return self.tokens[self.cursor + number]
    
    def prev(self, number=1):
        return self.tokens[self.cursor - number]        
    
    def hasMore(self, count=1):
        return self.cursor + count < len(self.tokens)
    
    def hasCurrent(self):
        return self.cursor < len(self.tokens)
    
    def ahead(self):
        self.cursor += 1        
    
    def snapshot(self):
        self.snapshot = self.cursor
        
    def reset(self):
        self.cursor = self.snapshot
        return self.tokens[self.cursor]
    
    def __str__(self):
        return f"[Cursor: {self.cursor}\n{', '.join([str(token) for token in self.tokens])}]"
    
    def __repr__(self):
        return self.__str__()
