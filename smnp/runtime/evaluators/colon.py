from smnp.ast.node.integer import IntegerLiteralNode
from smnp.ast.node.note import NoteLiteralNode
from smnp.error.runtime import RuntimeException
from smnp.note.model import Note
from smnp.type.model import Type
from smnp.type.value import Value


def evaluateColon(colon, environment):
    if isinstance(colon.a, NoteLiteralNode) and isinstance(colon.b, NoteLiteralNode):
        return Value(Type.LIST, [Value(Type.NOTE, n) for n in Note.range(colon.a.value, colon.b.value)])

    elif isinstance(colon.a, IntegerLiteralNode) and isinstance(colon.b, IntegerLiteralNode):
        return Value(Type.LIST, [Value(Type.INTEGER, i) for i in range(colon.a.value, colon.b.value + 1)])

    raise RuntimeException("Invalid colon arguments", colon.pos)