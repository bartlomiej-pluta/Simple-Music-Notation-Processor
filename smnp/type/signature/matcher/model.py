class Matcher:
    def __init__(self, objectType, matcher, string):
        self.type = objectType
        self.matcher = matcher
        self.string = string

    def match(self, value):
        if self.type is not None and self.type != value.type:
            return False
        return self.matcher(value)

    def andWith(self, matcher):
        if self.type != matcher.type:
            raise RuntimeError("Support types of matches are not the same")
        string = f"[{self.string} and {matcher.string}]"
        return Matcher(self.type, lambda x: self.match(x) and matcher.match(x), string)

    def orWith(self, matcher):
        string = f"[{self.string} or {matcher.string}]"
        return Matcher(None, lambda x: self.match(x) or matcher.match(x), string)

    def __eq__(self, other):
        return self.type == other.type and self.string == other.string

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()