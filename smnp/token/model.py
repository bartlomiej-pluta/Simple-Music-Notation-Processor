class Token:
    def __init__(self, type, value, pos, rawValue=None):
        self.type = type
        self.value = value    
        self.pos = pos
        if rawValue is None:
            rawValue = value
        self.rawValue = rawValue

    def __str__(self):
        return "Token(" + str(self.type) + ", '" + str(self.value) + "', " + str(self.pos) + ")"

    def __repr__(self):
        return self.__str__()


class TokenList:
    def __init__(self, tokens, lines):
        self.tokens = tokens
        self.cursor = 0
        self.snap = 0
        self.lines = lines
        
    def append(self, token):
        self.tokens.append(token)
        
    def __getitem__(self, index):
        return self.tokens[index]
    
    def current(self):
        if self.cursor >= len(self.tokens):
            raise RuntimeError(f"Cursor points to not existing token! Cursor = {self.cursor}, len = {len(self.tokens)}")
        return self.tokens[self.cursor]

    def currentPos(self):
        #TODO maybe change raw pos (position) tuple to some class with method "nextCol()", "nextRow()" etc.
        return self.current().pos if self.hasCurrent() else (self.tokens[-1].pos[0], self.tokens[-1].pos[1]+1) if len(self.tokens) > 0 else None

    def isCurrent(self, type):
        return self.hasCurrent() and self.current().type == type

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
        return self.cursor
        
    def reset(self, snap):
        self.cursor = snap

    def currentToEndOfLine(self):
        return self.lines[self.current().pos[0]][self.current().pos[1]:]

    def __str__(self):
        return f"[Current({self.cursor}): {self.current() if self.hasCurrent() else 'out of tokens'}\n{', '.join([str(token) for token in self.tokens])}]"
    
    def __repr__(self):
        return self.__str__()
