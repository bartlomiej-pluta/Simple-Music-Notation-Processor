import re

from smnp.token.model import Token


def regexPatternTokenizer(type, pattern):
    def tokenizer(input, current, line):
        consumedChars = 0
        value = ''

        while current+consumedChars < len(input) and re.match(pattern, input[current+consumedChars]):
            value += input[current+consumedChars]
            consumedChars += 1
        return (consumedChars, Token(type, value, (line, current)) if consumedChars > 0 else None)

    return tokenizer


def keywordsTokenizer(type, *keywords, mapKeyword=lambda x: x):
    def tokenizer(input, current, line):
        for keyword in keywords:
            result = keywordTokenizer(type, keyword, mapKeyword)(input, current, line)
            if result[0] > 0:
                return result
        return (0, None)

    return tokenizer


def keywordTokenizer(type, keyword, mapKeyword=lambda x: x):
    def tokenizer(input, current, line):
        if len(input) >= current+len(keyword) and input[current:current+len(keyword)] == keyword:
            return (len(keyword), Token(type, mapKeyword(keyword), (line, current)))
        return (0, None)
    return tokenizer


def defaultTokenizer(type):
    return keywordTokenizer(type, type.key)


def separated(tokenizer, end=r"\W"):
    def separated(input, current, line):
        consumedChars, token = tokenizer(input, current, line)
        if consumedChars > 0:
            if len(input) > current+consumedChars and re.match(end, input[current+consumedChars]):
                return (consumedChars, token)
            if len(input) == current+consumedChars:
                return (consumedChars, token)
        return (0, None)

    return separated
