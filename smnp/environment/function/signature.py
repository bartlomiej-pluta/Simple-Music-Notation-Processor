# from smnp.type.model import Type
#
from smnp.type.model import Type


class Matcher:
    def __init__(self, objectType, matcher):
        self.type = objectType
        self.matcher = matcher

    def match(self, value):
        if self.type is not None and self.type != value.type:
            return False
        return self.matcher(value)

    def andWith(self, matcher):
        if self.type != matcher.type:
            raise RuntimeError("Support types of matches are not the same")
        return Matcher(self.type, lambda x: self.matcher(x) and matcher.matcher(x))


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
    return check


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

    return check


def doesNotMatch(sign):
    return (False, *[None for n in sign])


def ofTypes(*types):
    def check(value):
        return value.type in types
    return Matcher(None, check)


def listOf(*types):
    def check(value):
        return len([item for item in value.value if not item.type in types]) == 0

    return Matcher(Type.LIST, check)


def listMatches(*pattern):
    def check(value):
        return signature(pattern)(value.value)[0]

    return Matcher(Type.LIST, check)


def recursiveListMatcher(matcher):
    if matcher.type == Type.LIST:
        raise RuntimeError(f"Passed matcher will be handling non-list types, so it cannot have type set to {Type.LIST}")

    def check(value):
        if value.type != Type.LIST:
            return matcher.match(value)
        for item in value.value:
            return check(item)

    return Matcher(Type.LIST, check)

