from functools import reduce


def combine(args, env):
    if all(type(x) == list for x in args):
        return reduce((lambda x, y: x + y), args)


def flat(args, env):
    return _flat(args, [])


def _flat(input, output = []):
    for item in input:
        if type(item) == list:
            _flat(item, output)
        else:
            output.append(item)
    return output
