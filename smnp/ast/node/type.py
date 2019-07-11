# from smnp.ast.node.iterable import abstractIterableParser
# from smnp.ast.node.model import Node
# from smnp.ast.node.operator import LeftAssociativeOperatorNode
# from smnp.ast.parser import Parser
# from smnp.token.type import TokenType
# from smnp.type.model import Type
#
from smnp.ast.node.atom import TypeLiteralParser
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.node.none import NoneNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class Type(Node):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = [NoneNode(), NoneNode()]

    @property
    def type(self):
        return self[0]

    @type.setter
    def type(self, value):
        self[0] = value

    @property
    def specifiers(self):
        return self[1]

    @specifiers.setter
    def specifiers(self, value):
        self[1] = value

    @classmethod
    def withValues(cls, pos, type, specifiers=NoneNode()):
        node = cls(pos)
        node.type = type
        node.specifiers = specifiers
        return node


class TypesList(Node):
    pass


def TypesListParser(input):
    typeListItem = Parser.oneOf(
        TypeParser
    )

    return abstractIterableParser(
        TypesList,
        TokenType.OPEN_ANGLE,
        TokenType.CLOSE_ANGLE,
        TypeParser
    )(input)


class TypeSpecifiers(Node):
    pass


def TypeParser(input):
    typeWithSpecifier = Parser.allOf(
        TypeLiteralParser,
        Parser.many(TypesListParser, createNode=TypeSpecifiers.withChildren),
        createNode=lambda type, specifiers: Type.withValues(type.pos, type, specifiers),
        name="type with specifiers?"
    )

    return Parser.oneOf(
        typeWithSpecifier,
        TypesListParser,
        name="mult. types or type with specifier"
    )(input)


# class TypeSpecifier(Node):
#
#     @classmethod
#     def _parse(cls, input):
#         return abstractIterableParser(TypeSpecifier, TokenType.OPEN_ANGLE, TokenType.CLOSE_ANGLE,
#                                       Parser.doAssert(cls._specifierItem(), "type"))(input)
#
#     @classmethod
#     def _specifierItem(cls):
#         return Parser.oneOf(
#             TypeNode.parse,
#             cls.parse
#         )
#
# class TypeSpecifiers(Node):
#     pass
#
#
# class TypeNode(LeftAssociativeOperatorNode):
#     def __init__(self, pos):
#         super().__init__(pos)
#
#     @property
#     def type(self):
#         return self[0]
#
#     @type.setter
#     def type(self, value):
#         self[0] = value
#
#     @property
#     def specifiers(self):
#         return self[1]
#
#     @specifiers.setter
#     def specifiers(self, value):
#         self[1] = value
#
#     @classmethod
#     def _parse(cls, input):
#         def createNode(type, specifiers):
#             node = TypeNode(type.pos)
#             node.type = Type[type.value.upper()]
#             node.specifiers = specifiers
#             return node
#
#         return Parser.allOf(
#             cls._rawTypeParser(),
#             Parser.many(TypeSpecifier.parse, lambda specifiers, pos: TypeSpecifiers.withChildren(specifiers, pos)),
#             createNode=createNode
#         )(input)
#
#     @classmethod
#     def _rawTypeParser(cls):
#         return Parser.terminalParser(TokenType.TYPE, lambda val, pos: TypeNode.withValue(val, pos))