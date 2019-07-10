from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.node.model import ParseResult, Node
from smnp.ast.node.none import NoneNode
from smnp.ast.node.operator import OperatorNode
from smnp.error.syntax import SyntaxException


def parse(input):
    from smnp.ast.node.program import Program
    return Program.parse(input).node


class Parser:

    # a -> A
    @staticmethod
    def terminalParser(expectedType, createNode=None, doAssert=False):
        def provideNode(value, pos):
            if createNode is None:
                return IgnoredNode(pos)
            return createNode(value, pos)

        def parse(input):
            if input.hasCurrent() and input.current().type == expectedType:
                token = input.current()
                input.ahead()
                return ParseResult.OK(provideNode(token.value, token.pos))
            elif doAssert:
                found = f", found '{input.current().rawValue}'" if input.hasCurrent() else ""
                raise SyntaxException(f"Expected '{expectedType.key}'{found}", input.currentPos())

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
                input.reset(snap)

            if exception is not None:
                if callable(exception):
                    raise exception(input)
                else:
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
                        if callable(exception):
                            raise exception(input)
                        else:
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
            oneAtLeast = False
            if left.result:
                operator = Parser.terminalParser(operatorTokenType, lambda val, pos: OperatorNode.withChildren([val], pos))(input)
                while operator.result:
                    oneAtLeast = True
                    right = rightParser(input)
                    left = ParseResult.OK(createNode(left.node, operator.node, right.node))
                    operator = Parser.terminalParser(operatorTokenType)(input)
                if oneAtLeast:
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

    @staticmethod
    def doAssert(parser, expected):
        def parse(input):
            result = parser(input)

            if not result.result:
                found = f", found '{input.current().rawValue}'" if input.hasCurrent() else ''

                raise SyntaxException(f"Expected {expected}{found}", input.currentPos())

            return result

        return parse

    @staticmethod
    def optional(parser):
        def parse(input):
            result = parser(input)
            if result.result:
                return result

            return ParseResult.OK(NoneNode())

        return parse

    @staticmethod
    def many(parser, createNode):
        def parse(input):
            results = []
            snap = input.snapshot()
            pos = input.currentPos()
            while True:
                result = parser(input)
                if result.result:
                    results.append(result.node)
                    snap = input.snapshot()
                else:
                    input.reset(snap)
                    return ParseResult.OK(createNode(results, pos) if len(results) > 0 else NoneNode())

        return parse
