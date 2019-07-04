from smnp.error.function import FunctionNotFoundException, MethodNotFoundException
from smnp.error.runtime import RuntimeException


class Environment():
    def __init__(self, scopes, functions, methods):
        self.scopes = scopes
        self.functions = functions
        self.methods = methods
        self.customFunctions = {}
        self.callStack = [] #TODO remove

    def invokeMethod(self, name, object, args):
        for method in self.methods: # TODO to działa tylko dla wbudowanych funkcji
            if method.name == name:
                ret = method.call(self, [object, *args])
                if ret is not None:
                    return ret
        raise MethodNotFoundException(object.type, name) # TODO method not found

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
        raise RuntimeException(f"Variable '{name}' is not declared" + (
            "" if type is None else f" (expected type: {type})"), pos)

    def findVariableScope(self, name, type=None):
        for scope in reversed(self.scopes):
            if name in scope:
                if type is not None:
                    if isinstance(scope[name], type):
                        return scope
                else:
                    return scope

    def scopesToString(self):
        return "Scopes:\n" + ("\n".join([ f"  [{i}]: {scope}" for i, scope in enumerate(self.scopes) ]))

    def functionsToString(self):
        return "Functions:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.functions ]))

    def methodsToString(self):
        return "Methods:\n" + ("\n".join([f"  {function.name}(...)" for function in self.methods]))


    def __str__(self):
        return self.scopesToString() + self.functionsToString() + self.methodsToString()

    def __repr__(self):
        return self.__str__()