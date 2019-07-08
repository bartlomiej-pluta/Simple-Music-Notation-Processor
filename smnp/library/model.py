from enum import Enum, auto

from smnp.error.function import IllegalFunctionInvocationException
from smnp.type.model import Type


class FunctionType(Enum):
    FUNCTION = auto()
    METHOD = auto()


class Function:
    def __init__(self, signature, function, name=None):
        self.name = name
        self.signature = signature
        self.function = function

    def stringSignature(self):
        return f"{self.name}{self.signature.string}"

    def call(self, env, args):
        result = self.signature.check(args)
        if result[0]:
            ret = self.function(env, *result[1:])
            if ret is None:
                return Type.void()
            return ret
        raise IllegalFunctionInvocationException(self.stringSignature(), f"{self.name}{types(args)}") #TODO: argumenty do typów, nie wartości


class CombinedFunction(Function):
    def __init__(self, name, *functions):
        super().__init__(None, None, None)
        self.name = name
        self.functions    = functions

    def stringSignature(self):
        return "\nor\n".join([f"{self.name}{function.signature.string}" for function in self.functions])

    def call(self, env, args):
        for function in self.functions:
            result = function.signature.check(args)
            if result[0]:
                ret = function.function(env, *result[1:])
                if ret is None:
                    return Type.void()
                return ret
        raise IllegalFunctionInvocationException(self.stringSignature(), f"{self.name}{types(args)}")


def types(args, parentheses=True):
    output = []
    for arg in args:
        if arg.type == Type.LIST:
            output.append(listTypes(arg.value, []))
        else:
            output.append(arg.type.name.lower())
    return f"({', '.join(output)})" if parentheses else ', '.join(output)


def listTypes(l, output=None):
    if output is None:
        output = []
    for item in l:
        if item.type == Type.LIST:
            output.append(listTypes(item.value, []))
        else:
            output.append(item.type.name.lower())
    return f"{Type.LIST.name.lower()}<{', '.join(set(output))}>"