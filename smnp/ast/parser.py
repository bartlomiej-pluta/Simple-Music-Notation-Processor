from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.node.model import ParseResult, Node
from smnp.ast.node.none import NoneNode
from smnp.error.syntax import SyntaxException


def parse(input):
    from smnp.ast.node.program import ProgramParser
    return ProgramParser(input).node


class Parser:
    def __init__(self, parse, name=None, parsers=None):
        if parsers is None:
            parsers = []
        self.parsers = parsers

        self._parse = parse
        if name is None:
            name = parse.__name__
        self.name = name

    def parse(self, input):
        result = self._parse(input)
        if result is None:
            return ParseResult.FAIL()

        if not isinstance(result, ParseResult):
            raise RuntimeError(f"_parse() method of '{self.__class__.__name__}' class haven't returned ParseResult object")

        return result

    def __call__(self, input):
        return self.parse(input)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    # a -> A
    @staticmethod
    def terminal(expectedType, createNode=None, doAssert=False):
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

        return Parser(parse, name=expectedType.name.lower())

    # oneOf -> a | b | c | ...
    @staticmethod
    def oneOf(*parsers, assertExpected=None, exception=None, name="or"):
        def combinedParser(input):
            snap = input.snapshot()
            for parser in parsers:
                value = parser(input)
                if value.result:
                    return value
                input.reset(snap)

            if assertExpected is not None:
                found = f", found '{input.current().rawValue}'" if input.hasCurrent() else ""
                raise SyntaxException(f"Expected {assertExpected}{found}", input.currentPos())

            if exception is not None:
                if callable(exception):
                    raise exception(input)
                else:
                    raise exception

            input.reset(snap)
            return ParseResult.FAIL()

        return Parser(combinedParser, name=name, parsers=parsers)

    # allOf -> a b c ...
    @staticmethod
    def allOf(*parsers, createNode, exception=None, name="all"):
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


        return Parser(extendedParser, name=name, parsers=parsers)


    # leftAssociative -> left | left OP right
    @staticmethod
    def leftAssociativeOperatorParser(leftParser, operatorTokenTypes, rightParser, createNode, name="leftAssoc"):
        from smnp.ast.node.operator import Operator

        def parse(input):
            operatorParser = Parser.oneOfTerminals(*operatorTokenTypes, createNode=lambda val, pos: Operator.withChildren([val], pos))
            left = leftParser(input)
            if left.result:
                operator = operatorParser(input)
                while operator.result:
                    right = rightParser(input)
                    left = ParseResult.OK(createNode(left.node, operator.node, right.node))
                    operator = operatorParser(input)
                return left

            return ParseResult.FAIL()

        return Parser(parse, name=name, parsers=[leftParser, '|'.join([t.value for t in operatorTokenTypes]), rightParser])

    @staticmethod
    def oneOfTerminals(*tokenTypes, createNode=None):
        return Parser.oneOf(*[Parser.terminal(expectedType, createNode=createNode) for expectedType in tokenTypes], name='|'.join([t.value for t in tokenTypes]))

    # loop -> start item* end
    @staticmethod
    def loop(startParser, itemParser, endParser, createNode, name="loop"):
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

        return Parser(parse, name, parsers=[startParser, itemParser, endParser])

    @staticmethod
    def doAssert(parser, expected, name="!!"):
        def parse(input):
            result = parser(input)

            if not result.result:
                found = f", found '{input.current().rawValue}'" if input.hasCurrent() else ''

                raise SyntaxException(f"Expected {expected}{found}", input.currentPos())

            return result

        return Parser(parse, name, parsers=parser)

    @staticmethod
    def optional(parser, name="??"):
        def parse(input):
            result = parser(input)
            if result.result:
                return result

            return ParseResult.OK(NoneNode())

        return Parser(parse, name, parsers=[parser])

    @staticmethod
    def epsilon():
        return lambda *args: ParseResult.OK(NoneNode())

    @staticmethod
    def many(parser, createNode, name="*"):
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

        return Parser(parse, name, parsers=[parser])

    @staticmethod
    def wrap(parser, createNode):
        def parse(input):
            result = parser(input)
            if result.result:
                return ParseResult.OK(createNode(result.node))

            return result

        return parse