from smnp.ast.parser import Parser


def SingletonParser(function):
    def wrapper(*args, **kwargs):
        if not hasattr(function, 'instance'):
            function.instance = function(*args, **kwargs)

        if not isinstance(function.instance, Parser):
            raise RuntimeError(f"Function {function.__name__} haven't returned Parser object")

        return function.instance

    return wrapper