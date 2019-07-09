from smnp.library.signature import signature
from smnp.type.model import Type
from smnp.type.signature.matcher.model import Matcher


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