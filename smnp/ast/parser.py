from smnp.ast.node.ignore import IgnoredNode
from smnp.ast.node.model import ParseResult, Node
from smnp.ast.node.none import NoneNode
from smnp.error.syntax import SyntaxException


def parse(input):
    from smnp.ast.node.program import ProgramParser
    return ProgramParser(input).node


class Parser(object):
    def __init__(self, name):
        self.name = name

    def parse(self, input):
        result = self._parse(input)
        if result is None:
            return ParseResult.FAIL()

        if not isinstance(result, ParseResult):
            raise RuntimeError(
                f"_parse() method of '{self.__class__.__name__}' class haven't returned ParseResult object")

        return result

    def _parse(self, input):
        raise RuntimeError(f"_name method of '{self.__class__.__name__}' class is not implemented")

    def grammar(self):
        rules = []
        self._grammarRules(rules)
        return "\n".join(self._uniq(rules))

    def _uniq(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def _grammarRules(self, output):
        output.append(f"class '{self.__class__.__name__}' does not implement _grammarRules() method")

    def __call__(self, input):
        return self.parse(input)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Parsers:

    @staticmethod
    def terminal(expectedType, createNode=lambda val, pos: IgnoredNode(pos), doAssert=False):
        return TerminalParser(expectedType, createNode, doAssert)

    @staticmethod
    def oneOf(*parsers, name, exception=None):
        return OneOfParser(*parsers, name=name, exception=exception)

    @staticmethod
    def allOf(*parsers, createNode, exception=None, name):
        return AllOfParser(*parsers, createNode=createNode, exception=exception, name=name)

    @staticmethod
    def leftAssociativeOperatorParser(leftParser, operatorTokenTypes, rightParser, createNode, name):
        return LeftAssociativeOperatorParser(leftParser, operatorTokenTypes, rightParser, createNode, name)

    @staticmethod
    def many(itemParser, createNode, name):
        return ManyParser(itemParser, createNode, name)

    @staticmethod
    def optional(parser, name):
        return OptionalParser(parser, name)

    @staticmethod
    def loop(startParser, itemParser, endParser, createNode, name):
        return LoopParser(startParser, itemParser, endParser, createNode, name)


class DecoratorParser(Parser):
    def __init__(self, wrapper, parser):
        super().__init__(parser.name)
        self.wrapper = wrapper
        self.parser = parser
        self._grammarRules = parser._grammarRules

    def _parse(self, input):
        result = self.parser.parse(input)
        return self.wrapper(result)


class TerminalParser(Parser):

    def __init__(self, expectedType, createNode=lambda val, pos: IgnoredNode(pos), doAssert=False):
        super().__init__(expectedType.name.lower())
        self.expectedType = expectedType
        self.createNode = createNode
        self.doAssert = doAssert

    def _grammarRules(self, output):
        output.append(f"{self.name} -> '{self.expectedType.value}'")

    def _parse(self, input):
        if input.isCurrent(self.expectedType):
            token = input.current()
            input.ahead()
            return ParseResult.OK(self.createNode(token.value, token.pos))
        elif self.doAssert:
            found = f", found '{input.current().rawValue}'" if input.hasCurrent() else ""
            raise SyntaxException(f"Expected '{self.expectedType.key}'{found}", input.currentPos())

        return ParseResult.FAIL()



class OneOfParser(Parser):
    def __init__(self, *parsers, name, exception=None):
        super().__init__(name)
        self.parsers = parsers
        self.exception = exception

    def _parse(self, input):
        snap = input.snapshot()
        for parser in self.parsers:
            value = parser.parse(input)
            if value.result:
                return value
            input.reset(snap) # TODO sprawdzic, czy koneiczne !!!!!

        if self.exception is not None:
            if callable(self.exception):
                raise self.exception(input)
            else:
                raise self.exception

        return ParseResult.FAIL()

    def _grammarRules(self, output):
        output.extend([ f"{self.name} -> {parser.name}" for parser in self.parsers ])
        [ parser._grammarRules(output) for parser in self.parsers ]


class AllOfParser(Parser):
    def __init__(self, *parsers, createNode, exception=None, name):
        super().__init__(name)

        if len(parsers) == 0:
            raise RuntimeError("Pass one parser at least")

        self.parsers = parsers
        self.createNode = createNode
        self.exception = exception

    def _parse(self, input):
        snap = input.snapshot()
        parsedItems = []

        for parser in self.parsers:
            result = parser.parse(input)

            if not result.result:
                if self.exception is not None:
                    if callable(self.exception):
                        raise self.exception(input)
                    else:
                        raise self.exception

                input.reset(snap)
                return ParseResult.FAIL()

            parsedItems.append(result.node)

        node = self.createNode(*parsedItems)
        if not isinstance(node, Node):
            raise RuntimeError(f"Method 'createNode' of class '{self.__class__.__name__}' haven't returned a Node object. Probably forget to pass 'return'")

        return ParseResult.OK(node)

    def _grammarRules(self, output):
        output.append(self.name + ' -> ' + ' '.join([ parser.name for parser in self.parsers ]))
        [ parser._grammarRules(output) for parser in self.parsers ]


class LeftAssociativeOperatorParser(Parser):
    def __init__(self, leftParser, operatorTokenTypes, rightParser, createNode, name):
        from smnp.ast.node.operator import Operator

        super().__init__(name)
        self.leftParser = leftParser
        self.rightParser = rightParser
        self.createNode = createNode
        self.operators = operatorTokenTypes

        operatorParsers = [ TerminalParser(expectedType, createNode=lambda val, pos: Operator.withValue(val, pos)) for expectedType in operatorTokenTypes ]
        self.operatorParser = OneOfParser(*operatorParsers, name="not important")

    def _parse(self, input):
        snap = input.snapshot()
        left = self.leftParser.parse(input)
        if left.result:
            operator = self.operatorParser.parse(input)
            while operator.result:
                right = self.rightParser.parse(input)
                left = ParseResult.OK(self.createNode(left.node, operator.node, right.node))
                operator = self.operatorParser.parse(input)
            return left

        return ParseResult.FAIL()


    def _grammarRules(self, output):
        output.append('\n'.join([f"{self.name} -> {self.leftParser.name} {operator.name.lower()} {self.rightParser.name} | {self.leftParser.name}" for operator in self.operators]))
        self.leftParser._grammarRules(output)
        self.rightParser._grammarRules(output)


class ManyParser(Parser):
    def __init__(self, itemParser, createNode, name):
        super().__init__(name)
        self.itemParser = itemParser
        self.createNode = createNode

    def _parse(self, input):
        snap = input.snapshot()

        parsedItems = []
        pos = input.currentPos()
        while True:
            result = self.itemParser.parse(input)
            if result.result:
                parsedItems.append(result.node)
                snap = input.snapshot()
            else:
                input.reset(snap)
                return ParseResult.OK(self.createNode(parsedItems, pos) if len(parsedItems) > 0 else NoneNode())

    def _grammarRules(self, output):
        output.append(f"{self.name} -> {self.itemParser.name}*")
        self.itemParser._grammarRules(output)


class OptionalParser(Parser):
    def __init__(self, parser, name):
        super().__init__(name)
        self.parser = parser

    def _parse(self, input):
        result = self.parser.parse(input)
        if result.result:
            return result

        return ParseResult.OK(NoneNode())

    def _grammarRules(self, output):
        output.append(f"{self.name} -> {self.parser.name}?")


class LoopParser(Parser):
    def __init__(self, startParser, itemParser, endParser, createNode, name):
        super().__init__(name)
        self.startParser = startParser
        self.itemParser = itemParser
        self.endParser = endParser
        self.createNode = createNode

    def _parse(self, input):
        items = []
        start = self.startParser.parse(input)
        if start.result:
            while True:
                end = self.endParser.parse(input)
                if end.result:
                    return ParseResult.OK(self.createNode(start.node, items, end.node))
                item = self.itemParser.parse(input)
                if not item.result:
                    return ParseResult.FAIL()
                items.append(item.node)

        return ParseResult.FAIL()

    def _grammarRules(self, output):
        output.append(f"{self.name} -> {self.startParser.name} {self.itemParser.name}* {self.endParser.name}")
        self.startParser._grammarRules(output)
        self.itemParser._grammarRules(output)
        self.endParser._grammarRules(output)

