from smnp.type.model import Type


def argsTypesToString(args, parentheses=True):
    output = []
    for arg in args:
        if arg.type == Type.LIST:
            output.append(listTypes(arg.value, []))
        elif arg.type == Type.MAP:
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