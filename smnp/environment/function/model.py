from enum import Enum, auto


class FunctionType(Enum):
    FUNCTION = auto()
    METHOD = auto()


class Function:
    def __init__(self, signature, function):
        self.signature = signature
        self.function = function

    def call(self, env, args):
        result = self.signature(args)
        if result[0]:
            return self.function(env, *result[1:])
        # todo: raise illegal signature exception or something