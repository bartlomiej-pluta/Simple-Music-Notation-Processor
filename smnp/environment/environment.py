from smnp.error.function import FunctionNotFoundException
from smnp.error.runtime import RuntimeException


class Environment():
    def __init__(self, scopes, functions, methods):
        self.scopes = scopes
        self.functions = functions
        self.methods = methods
        self.customFunctions = {}
        self.callStack = [] #TODO remove

    def invokeFunction(self, name, args):
        for function in self.functions: # TODO to działa tylko dla wbudowanych funkcji
            if function.name == name:
                ret = function.call(self, args)
                if ret is not None:
                    return ret
        raise FunctionNotFoundException(name)
        # TODO raise nie znaleziono funkcji

    def findVariable(self, name, type=None, pos=None):
        for scope in reversed(self.scopes):
            if name in scope:
                value = scope[name]
                if type is not None:
                    if isinstance(value, type):
                        return value
                else:
                    return value
        raise RuntimeException(pos, f"Variable '{name}' is not declared" + (
            "" if type is None else f" (expected type: {type})"))

    def findVariableScope(self, name, type=None):
        for scope in reversed(self.scopes):
            if name in scope:
                if type is not None:
                    if isinstance(scope[name], type):
                        return scope
                else:
                    return scope