from smnp.environment.environment import Environment
from smnp.module import functions, methods
from smnp.type.model import Type


def createEnvironment():
    variables = {
        "bpm": Type.integer(120)
    }

    return Environment([ variables ], functions, methods)
 
