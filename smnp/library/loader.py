from pkg_resources import resource_string

from smnp.program.interpreter import Interpreter


def loadStandardLibrary():
    mainSource = resource_string('smnp.library.code', 'main.mus').decode("utf-8")
    boolSource = resource_string('smnp.library.code', 'bool.mus').decode("utf-8")
    env = Interpreter.interpretString(mainSource)
    return Interpreter.interpretString(boolSource, baseEnvironment=env)

