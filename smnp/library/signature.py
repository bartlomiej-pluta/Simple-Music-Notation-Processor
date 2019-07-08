# from smnp.type.model import Type
#
from smnp.type.model import Type


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



    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()


class Signature:
    def __init__(self, check, string):
        self.check = check
        self.string = string


def varargSignature(varargMatcher, *basicSignature):
    def check(args):
        if len(basicSignature) > len(args):
            return doesNotMatchVararg(basicSignature)

        for i in range(len(basicSignature)):
            if not basicSignature[i].match(args[i]):
                return doesNotMatchVararg(basicSignature)

        for i in range(len(basicSignature), len(args)):
            if not varargMatcher.match(args[i]):
                return doesNotMatchVararg(basicSignature)

        return True, (*args[:len(basicSignature)]), args[len(basicSignature):]

    string = f"({', '.join([str(m) for m in basicSignature])}{', ' if len(basicSignature) > 0 else ''}{str(varargMatcher)}...)"

    return Signature(check, string)


def doesNotMatchVararg(basicSignature):
    return (False, *[None for n in basicSignature], None)
#


def signature(*signature):
    def check(args):
        if len(signature) != len(args):
            return doesNotMatch(signature)

        for s, a in zip(signature, args):
            if not s.match(a):
                return doesNotMatch(signature)

        return (True, *args)

    string = f"({', '.join([str(m) for m in signature])})"

    return Signature(check, string)


def doesNotMatch(sign):
    return (False, *[None for n in sign])


def allTypes():
    allowedTypes = [t for t in Type if t != Type.VOID]
    return ofTypes(*allowedTypes)


def ofTypes(*types):
    def check(value):
        return value.type in types
    return Matcher(None, check, f"<{', '.join([t.name.lower() for t in types])}>")

def ofType(type):
    def check(value):
        return value.type == type

    return Matcher(None, check, type.name.lower())

def listOf(*types):
    def check(value):
        return len([item for item in value.value if not item.type in types]) == 0

    return Matcher(Type.LIST, check, f"{Type.LIST.name.lower()}<{', '.join([t.name.lower() for t in types])}>")

def listOfMatchers(*matchers):
    def check(value):
        matched = 0
        for item in value.value:
            matched += 1 if any(matcher.match(item) for matcher in matchers) else 0

        return matched == len(value.value)

    return Matcher(Type.LIST, check, f"{Type.LIST.name.lower()}<{', '.join([m.string for m in matchers])}>")

def listMatches(*pattern):
    def check(value):
        return signature(*pattern).check(value.value)[0]

    return Matcher(Type.LIST, check, f"({', '.join([str(m) for m in pattern])})")

def recursiveListMatcher(matcher):
    if matcher.type == Type.LIST:
        raise RuntimeError(f"Passed matcher will be handling non-list types, so it cannot have type set to {Type.LIST}")

    def check(value):
        if value.type != Type.LIST:
            return matcher.match(value)
        for item in value.value:
            return check(item)

    return Matcher(Type.LIST, check, f"[LISTS OF {str(matcher)}]")

