from smnp.environment.function.model import Function


def returnElementOrList(list):
    return list[0] if len(list) == 1 else list

def combineFunctions(*functions):
    if len(functions) == 0:
        raise RuntimeError("Must be passed one function at least")

    def signature(args):
        ret = None
        for fun in functions:
            ret = fun.signature(args)
            if ret[0] == True:
                return ret
        return ret

    def function(env, *args):
        originalArgs = removeFirstLevelNesting(args)
        for fun in functions:
            if fun.signature(originalArgs)[0]:
                return fun.function(env, *args)

        return None

    return Function(signature, function)

def removeFirstLevelNesting(l):
    flat = []
    for item in l:
        if type(item) == list:
            for i in item:
                flat.append(i)
        else:
            flat.append(item)

    return flat