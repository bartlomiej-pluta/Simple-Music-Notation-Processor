from smnp.type.model import Type
from smnp.type.signature.matcher.model import Matcher


def mapOfMatchers(keyMatchers, valueMatchers):
    def check(map):
        matched = 0
        for key, value in map.value.items():
            matched += 1 if any(matcher.match(key) for matcher in keyMatchers) \
                            and any(matcher.match(value) for matcher in valueMatchers) else 0

        return matched == len(map.value)

    return Matcher(Type.MAP, check, f"{Type.MAP.name.lower()}<{', '.join([m.string for m in keyMatchers])}><{', '.join([m.string for m in valueMatchers])}>")