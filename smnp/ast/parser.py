from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.node.model import ParseResult, Node


def parse(input):
    from smnp.ast.node.program import Program
    return Program.parse(input).node


class Parser:

    # a -> A
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

    # oneOf -> a | b | c | ...
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

    # allOf -> a b c ...
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

            node = createNode(*results)
            if not isinstance(node, Node):
                raise RuntimeError("Function 'createNode' haven't returned a Node object. Probably forget to pass 'return'")

            return ParseResult.OK(node)



        return extendedParser


    # leftAssociative -> left | left OP right
    @staticmethod
    def leftAssociativeOperatorParser(leftParser, operatorTokenType, rightParser, createNode):
        def parse(input):
            left = leftParser(input)
            if left.result:
                while Parser.terminalParser(operatorTokenType)(input).result:
                    right = rightParser(input)
                    left = ParseResult.OK(createNode(left.node, right.node))

                return left

            return ParseResult.FAIL()

        return parse

    # loop -> start item* end
    @staticmethod
    def loop(startParser, itemParser, endParser, createNode):
        def parse(input):
            items = []
            start = startParser(input)
            if start.result:
                while True:
                    end = endParser(input)
                    if end.result:
                        return ParseResult.OK(createNode(start.node, items, end.node))
                    item = itemParser(input)
                    if not item.result:
                        return ParseResult.FAIL()
                    items.append(item.node)

            return ParseResult.FAIL()

        return parse

