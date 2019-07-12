from pkg_resources import resource_string

from smnp.program.interpreter import Interpreter


def loadStandardLibrary():
    mainSource = resource_string('smnp.library.code', 'main.mus').decode("utf-8")
    env = Interpreter.interpretString(mainSource)
    return env
