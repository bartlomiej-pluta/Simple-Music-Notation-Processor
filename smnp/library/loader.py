from pkg_resources import resource_string

from smnp.program.interpreter import Interpreter


def loadStandardLibrary():
    source = resource_string('smnp.library.code', 'main.mus').decode("utf-8")
    return Interpreter.interpretString(source)

