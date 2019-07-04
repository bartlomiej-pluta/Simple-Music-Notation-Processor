import random as r


def random(args, env):
    if not all(isinstance(x, list) and len(x) == 2 and isinstance(x[0], float) for x in args):
        return # not valid signature
    if sum([x[0] for x in args]) != 1.0:
        return # not sums to 100%
    choice = r.random()
    acc = 0
    for e in args:
        acc += e[0]
        if choice <= acc:
            return e[1]


#TODO: sample