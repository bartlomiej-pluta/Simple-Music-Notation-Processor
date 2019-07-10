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
        from smnp.environment.environment import CallStackItem

        result = self.signature.check(args)
        if result[0]:
            env.callStack.append(CallStackItem(self.name))
            ret = self.function(env, *result[1:])
            env.callStack.pop(-1)
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
        from smnp.environment.environment import CallStackItem

        for function in self.functions:
            result = function.signature.check(args)
            if result[0]:
                env.callStack.append(CallStackItem(self.name))
                ret = function.function(env, *result[1:])
                env.callStack.pop(-1)
                if ret is None:
                    return Type.void()
                return ret
        raise IllegalFunctionInvocationException(self.stringSignature(), f"{self.name}{types(args)}")


def types(args, parentheses=True):
    output = []
    for arg in args:
        if arg.type == Type.LIST:
            output.append(listTypes(arg.value, []))
        if arg.type == Type.MAP:
            output.append(mapTypes(arg.value, {}))
        else:
            output.append(arg.type.name.lower())
    return f"({', '.join(output)})" if parentheses else ', '.join(output)


def listTypes(l, output=None):
    if output is None:
        output = []
    for item in l:
        if item.type == Type.LIST:
            output.append(listTypes(item.value, []))
        if item.type == Type.MAP:
            output.append(mapTypes(item.value, {}))
        else:
            output.append(item.type.name.lower())
    return f"{Type.LIST.name.lower()}<{', '.join(set(output))}>"

def mapTypes(map, output=None):
    if output is None:
        output = {}

    for k, v in map.items():
        if v.type == Type.LIST:
            output[k] = (listTypes(v.value, []))
        elif v.type == Type.MAP:
            output[k] = mapTypes(v.value, {})
        else:
            output[k] = v.type.name.lower()

    return f"{Type.MAP.name.lower()}<{', '.join(set([ k.type.name.lower() for k, v in output.items() ]))}><{', '.join(set([ str(v) for k, v in output.items() ]))}>"