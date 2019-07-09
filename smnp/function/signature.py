# from smnp.type.model import Type
#
from smnp.type.model import Type


class Signature:
    def __init__(self, check, string, matchers):
        self.check = check
        self.string = string
        self.matchers = matchers


def varargSignature(varargMatcher, *basicSignature, wrapVarargInValue=False):
    def check(args):
        if len(basicSignature) > len(args):
            return doesNotMatchVararg(basicSignature)

        for i in range(len(basicSignature)):
            if not basicSignature[i].match(args[i]):
                return doesNotMatchVararg(basicSignature)

        for i in range(len(basicSignature), len(args)):
            if not varargMatcher.match(args[i]):
                return doesNotMatchVararg(basicSignature)

        if wrapVarargInValue:
            return True, (*args[:len(basicSignature)]), Type.list(args[len(basicSignature):])
        else:
            return True, (*args[:len(basicSignature)]), args[len(basicSignature):]

    string = f"({', '.join([str(m) for m in basicSignature])}{', ' if len(basicSignature) > 0 else ''}{str(varargMatcher)}...)"

    return Signature(check, string, [varargMatcher, *basicSignature])


def doesNotMatchVararg(basicSignature):
    return (False, *[None for n in basicSignature], None)

def signature(*signature):
    def check(args):
        if len(signature) != len(args):
            return doesNotMatch(signature)

        for s, a in zip(signature, args):
            if not s.match(a):
                return doesNotMatch(signature)

        return (True, *args)

    string = f"({', '.join([str(m) for m in signature])})"

    return Signature(check, string, signature)


def doesNotMatch(sign):
    return (False, *[None for n in sign])


