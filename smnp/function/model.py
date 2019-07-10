from enum import Enum, auto

from smnp.error.function import IllegalFunctionInvocationException
from smnp.function.tools import argsTypesToString
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
        raise IllegalFunctionInvocationException(self.stringSignature(), f"{self.name}{argsTypesToString(args)}") #TODO: argumenty do typów, nie wartości


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
        raise IllegalFunctionInvocationException(self.stringSignature(), f"{self.name}{argsTypesToString(args)}")


