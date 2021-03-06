from smnp.error.function import FunctionNotFoundException, MethodNotFoundException, IllegalFunctionInvocationException
from smnp.error.runtime import RuntimeException
from smnp.function.tools import argsTypesToString
from smnp.runtime.evaluators.function import BodyEvaluator, Return
from smnp.type.model import Type


class Environment():
    def __init__(self, scopes, functions, methods, source):
        self.scopes = scopes
        self.functions = functions
        self.methods = methods
        self.customFunctions = []
        self.customMethods = []
        self.callStack = []
        self.source = source

    def invokeMethod(self, object, name, args):
        builtinMethodResult = self._invokeBuiltinMethod(object, name, args)
        if builtinMethodResult[0]:
            return builtinMethodResult[1]

        customMethodResult = self._invokeCustomMethod(object, name, args)
        if customMethodResult[0]:
            return customMethodResult[1]

        raise MethodNotFoundException(argsTypesToString([object], False), name)

    def _invokeBuiltinMethod(self, object, name, args):
        for method in self.methods:
            if method.name == name:
                ret = method.call(self, [object, *args])
                if ret is not None:
                    return (True, ret)

        return (False, None)

    def _invokeCustomMethod(self, object, name, args):
        for method in self.customMethods:
            if method.typeSignature.check([object])[0] and method.name == name: #Todo sprawdzic sygnature typu
                signatureCheckresult = method.signature.check(args)
                if signatureCheckresult[0]:
                    self.scopes.append(method.defaultArgs)
                    self.scopes[-1].update({argName: argValue for argName, argValue in zip(method.arguments, list(signatureCheckresult[1:]))})
                    self.scopes[-1][method.alias] = object
                    self.callStack.append(CallStackItem(name))
                    result = Type.void()
                    try:
                        BodyEvaluator.evaluate(method.body, self).value  # TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                    except Return as r:
                        result = r.value
                    self.callStack.pop(-1)
                    self.scopes.pop(-1)
                    return (True, result)
                raise IllegalFunctionInvocationException(f"{method.name}{method.signature.string}",
                                                         f"{name}{argsTypesToString(args)}")
        return (False, None)

    def invokeFunction(self, name, args):
        builtinFunctionResult = self._invokeBuiltinFunction(name, args)
        if builtinFunctionResult[0]:
            return builtinFunctionResult[1]

        customFunctionResult = self._invokeCustomFunction(name, args)
        if customFunctionResult[0]:
            return customFunctionResult[1]

        raise FunctionNotFoundException(name)

    def _invokeBuiltinFunction(self, name, args):
        for function in self.functions:
            if function.name == name:
                ret = function.call(self, args)
                if ret is not None:
                    return (True, ret)

        return (False, None)

    def _invokeCustomFunction(self, name, args):
        for function in self.customFunctions:
            if function.name == name:
                signatureCheckresult = function.signature.check(args)
                if signatureCheckresult[0]:
                    self.appendScope(function.defaultArgs)
                    appendedScopeIndex = len(self.scopes)-1
                    self.scopes[-1].update({ argName: argValue for argName, argValue in zip(function.arguments, list(signatureCheckresult[1:])) })
                    self.callStack.append(CallStackItem(name))
                    result = Type.void()
                    try:
                        BodyEvaluator.evaluate(function.body, self).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                    except Return as r:
                        result = r.value
                    self.callStack.pop(-1)
                    self.popScope(mergeVariables=False)
                    self.removeScopesAfter(appendedScopeIndex)
                    return (True, result)
                raise IllegalFunctionInvocationException(f"{function.name}{function.signature.string}", f"{name}{argsTypesToString(args)}")
        return (False, None)

    def addCustomFunction(self, name, signature, arguments, body, defaultArguments):
        if len([fun for fun in self.functions + self.customFunctions if fun.name == name]) > 0:
            raise RuntimeException(f"Cannot redeclare function '{name}'", None)

        self.customFunctions.append(CustomFunction(name, signature, arguments, body, defaultArguments))

    # TODO:
    # There is still problem with checking existing of generic types, like lists:
    # extend list as l {
    #   function foo() { return 1 }
    # }
    # extend list<integer> as l {
    #   function foo() { return 2 }
    # }
    # Then calling [1, 2, 3, 4].foo() will produce 1, when the second method is more suitable
    def addCustomMethod(self, typeSignature, alias, name, signature, arguments, body, defaultArguments):
        if len([m for m in self.methods if m.name == name and m.signature.matchers[0] == typeSignature.matchers[0]]) > 0:
            raise RuntimeException(f"Cannot redeclare method '{name}' for type '{typeSignature.matchers[0]}'", None)

        if len([m for m in self.customMethods if m.name == name and m.typeSignature.matchers[0] == typeSignature.matchers[0]]) > 0:
            raise RuntimeException(f"Cannot redeclare method '{name}' for type '{typeSignature.matchers[0]}'", None)

        self.customMethods.append(CustomMethod(typeSignature, alias, name, signature, arguments, body, defaultArguments))

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

    def appendScope(self, variables=None):
        if variables is None:
            variables = {}

        self.scopes.append(variables)

    def popScope(self, mergeVariables=True):
        lastScope = self.scopes.pop(-1)
        if mergeVariables:
            self.scopes[-1].update(lastScope)

    def removeScopesAfter(self, index):
        del self.scopes[index:]

    def scopesToString(self):
        return "Scopes:\n" + ("\n".join([ f"  [{i}]: {scope}" for i, scope in enumerate(self.scopes) ]))

    def functionsToString(self):
        return "Functions:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.functions ]))

    def customFunctionsToString(self):
        return "Custom Functions:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.customFunctions ]))

    def methodsToString(self):
        return "Methods:\n" + ("\n".join([f"  {function.name}(...)" for function in self.methods]))

    def customMethodsToString(self):
        return "Custom Methods:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.customMethods ]))

    def callStackToString(self):
        return "Call Stack:\n" + ("\n".join([ f"  [{i}]: {function.function}(...)" for i, function in reversed(list(enumerate(self.callStack))) ]))

    def extend(self, environment):
        self.scopes[0].update(environment.scopes[0])
        self.customFunctions.extend(environment.customFunctions)
        self.customMethods.extend(environment.customMethods)


    def __str__(self):
        return f"{self.scopesToString()}\n{self.functionsToString()}\n{self.methodsToString()}\n{self.customFunctionsToString()}\n{self.customMethodsToString()}\n{self.callStackToString()}"

    def __repr__(self):
        return self.__str__()


class CallStackItem:
    def __init__(self, function):
        self.function = function


class CustomFunction:
    def __init__(self, name, signature, arguments, body, defaultArgs):
        self.name = name
        self.signature = signature
        self.arguments = arguments
        self.body = body
        self.defaultArgs = defaultArgs


class CustomMethod:
    def __init__(self, typeSignature, alias, name, signature, arguments, body, defaultArgs):
        self.typeSignature = typeSignature
        self.alias = alias
        self.name = name
        self.signature = signature
        self.arguments = arguments
        self.body = body
        self.defaultArgs = defaultArgs