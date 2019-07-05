from smnp.newast.node.ignore import IgnoredNode
from smnp.newast.node.model import ParseResult


class Parser:

    @staticmethod
    def nonTerminalParser(parser, createNode):
        def parse(input):
            token = input.current()
            result = parse(input)
            if result.result:
                return ParseResult.OK(createNode(result.node, token.pos))
            return ParseResult.FAIL()
        return parse

    @staticmethod
    def terminalParser(expectedType, createNode=None):
        def provideNode(value, pos):
            if createNode is None:
                return IgnoredNode(pos)
            return createNode(value, pos)

        def parse(input):
            if input.hasCurrent() and input.current().type == expectedType:
                token = input.current()
                input.ahead()
                return ParseResult.OK(provideNode(token.value, token.pos))
            return ParseResult.FAIL()

        return parse

    @staticmethod
    def oneOf(*parsers, exception=None):
        def combinedParser(input):
            snap = input.snapshot()
            for parser in parsers:
                value = parser(input)
                if value.result:
                    return value

            if exception is not None:
                raise exception

            input.reset(snap)
            return ParseResult.FAIL()

        return combinedParser
    @staticmethod
    def allOf(*parsers, createNode, exception=None):
        if len(parsers) == 0:
            raise RuntimeError("Pass one parser at least")

        def extendedParser(input):
            snap = input.snapshot()

            results = []

            for parser in parsers:
                result = parser(input)

                if not result.result:
                    if exception is not None:
                        raise exception

                    input.reset(snap)
                    return ParseResult.FAIL()

                results.append(result.node)

            return ParseResult.OK(createNode(*results))



        return extendedParser
